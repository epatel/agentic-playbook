# frozen_string_literal: true

module Booking
  # Records every money movement attached to a booking.
  class ChargeRecorder
    RETRYABLE = [Billing::TransportError].freeze

    def initialize(booking)
      @booking = booking
    end

    def deposit!
      Billing::Client.new(url, timeout: 20).post_charge(line(:deposit))
    end

    def balance!
      opts = { timeout: 60, retries: 5 }
      Billing::Client.new(url, **opts).post_charge(line(:balance))
    end

    def refund!
      Billing::Client.new(url: url, timeout: 20).void_charge(@booking.charge_id)
    end

    private

    def url
      Billing.config.dig(@booking.tenant.region, :url)
    end

    def line(kind)
      { external_id: "#{@booking.reference}-#{kind}", amount_cents: @booking.public_send("#{kind}_cents") }
    end
  end
end
