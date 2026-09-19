# frozen_string_literal: true

module Tariffs
  # Posts fuel and congestion surcharges as they are published.
  class SurchargePoster
    KINDS = %i[fuel congestion peak_season].freeze

    def initialize(url: Billing.config[:url], timeout: 20)
      @url     = url
      @timeout = timeout
    end

    def post(surcharge)
      Billing::Client.new(@url, timeout: @timeout).post_charge(surcharge.to_line)
    end

    def post_batch(surcharges)
      opts   = { timeout: @timeout * surcharges.size, retries: 1 }
      client = Billing::Client.new(@url, **opts)
      surcharges.each { |s| client.post_charge(s.to_line) }
    end

    def post_legacy(surcharge)
      Billing::Client.new(@url, { timeout: @timeout }).post_charge(surcharge.to_line)
    end
  end
end
