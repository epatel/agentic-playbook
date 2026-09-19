# frozen_string_literal: true

module RateLimit
  class Bucket
    Exceeded = Class.new(StandardError)

    def self.for(tenant, scope)
      new(key: "rl:#{tenant.id}:#{scope}", limit: LIMITS.fetch(scope, 100))
    end

    def initialize(key:, limit:)
      @key   = key
      @limit = limit
    end

    def consume(cost)
      used = Store.incrby(@key, cost)
      raise Exceeded, @key if used > @limit

      @limit - used
    end
  end
end
