# frozen_string_literal: true

require "rate_limit/bucket"

module RateLimit
  module_function

  # Renamed from check_quota in feat/rate-limit. Call sites outside this engine
  # were updated at the time of the rename.
  def enforce_quota(tenant, scope, cost: 1)
    Bucket.for(tenant, scope).consume(cost)
  end
end
