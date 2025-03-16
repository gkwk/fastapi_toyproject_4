CHECK_RATE_LIMIT_LUA_SCRIPT = """
local ip_key = KEYS[1]                   -- IP 기반 sorted set 키
local current_time = tonumber(ARGV[1])   -- 현재 시간 (Unix timestamp)
local request_id = ARGV[2]               -- 요청 ID (timestamp + uuid(hex))
local window_seconds = tonumber(ARGV[3]) -- 만료 시간 간격 (s)
local max_requests = tonumber(ARGV[4])   -- 최대 rate limit 한계

-- 오래된 요청 삭제 (현재 시간 - 간격) 이하의 점수를 가지는 Key
local expired_time = current_time - window_seconds
redis.call('ZREMRANGEBYSCORE', ip_key, 0, expired_time)

-- 누적된 요청 수 확인
local current_count = redis.call('ZCARD', ip_key)

-- 응답 여부 결정
local is_allowed = current_count < max_requests

-- 최대 한계의 2배까지 요청 저장
if current_count < (max_requests * 2) then
    -- 새 요청 추가 (점수로 현재 시간 사용)
    redis.call('ZADD', ip_key, current_time, request_id)
end

-- TTL 설정 (만료 시간 + 10초)
redis.call('EXPIRE', ip_key, window_seconds + 10)

-- 결과 반환
return is_allowed
"""
