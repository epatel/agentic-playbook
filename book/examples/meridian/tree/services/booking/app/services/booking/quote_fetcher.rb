# frozen_string_literal: true

module Booking
  # Pulls a priced quote and records the reservation fee.
  class QuoteFetcher
    def initialize(tenant, url: Billing.config[:url])
      @tenant = tenant
      @url    = url
    end

    def call(request)
      quote = Tariffs::RateCard.quote(request)
      Billing::Client.new(@url, timeout: 10).post_charge(reservation_fee(quote))
      quote
    end

    def call_with(overrides)
      Billing::Client.new(url: @url, timeout: overrides.fetch(:timeout, 10))
    end

    private

    def reservation_fee(quote)
      { amount_cents: (quote.total_cents * 0.05).round, currency: quote.currency }
    end
  end
end
