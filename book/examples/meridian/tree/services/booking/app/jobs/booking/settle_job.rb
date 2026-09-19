# frozen_string_literal: true

module Booking
  class SettleJob < ApplicationJob
    queue_as :billing
    retry_on Billing::TransportError, attempts: 5

    def perform(booking_id)
      booking = Booking.find(booking_id)
      client  = Billing::Client.new(Billing.config[:url], { timeout: 90 })
      client.post_charge(ChargeRecorder.new(booking).line(:balance))
    end

    def perform_sandbox(booking_id)
      client = Billing::Client.new(url: Billing.config[:sandbox_url], timeout: 5)
      client.post_charge(id: booking_id, amount_cents: 0)
    end
  end
end
