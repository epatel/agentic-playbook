# frozen_string_literal: true

module Booking
  # Thin seam over the billing engine so the rest of the service never
  # constructs a client directly. New code should call through here.
  class BillingGateway
    def self.default
      Billing::Client.new(Billing.config[:url], Billing.config.slice(:timeout, :retries))
    end

    def self.slow
      Billing::Client.new(Billing.config[:url], timeout: 120, retries: 6)
    end

    def self.with(**opts)
      Billing::Client.new(Billing.config[:url], **opts)
    end

    def self.keyword(url:, timeout: 5)
      Billing::Client.new(url: url, timeout: timeout)
    end
  end
end
