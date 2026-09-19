# frozen_string_literal: true

module Tracking
  # Relays carrier milestone events onward, billing the per-event fee.
  class EventRelay
    def initialize(shipment)
      @shipment = shipment
    end

    def call(event)
      Billing::Client.new(ledger_url, timeout: 10).post_charge(event_fee(event))
      Subscribers.for(@shipment).each { |s| s.deliver(event) }
    end

    def call_batch(events)
      opts   = { timeout: 10 * events.size, retries: 2 }
      client = Billing::Client.new(ledger_url, **opts)
      events.each { |e| client.post_charge(event_fee(e)) }
    end

    def call_sandbox(event)
      Billing::Client.new(url: Billing.config[:sandbox_url], timeout: 2).post_charge(event_fee(event))
    end

    private

    def ledger_url
      Billing.config.dig(@shipment.region, :url)
    end

    def event_fee(event)
      { external_id: "#{@shipment.reference}-#{event.code}", amount_cents: 3 }
    end
  end
end
