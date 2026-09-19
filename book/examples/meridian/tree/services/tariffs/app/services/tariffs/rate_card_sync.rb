# frozen_string_literal: true

module Tariffs
  # Nightly sync of carrier rate cards, plus the ledger entries for the
  # per-card licensing fee each carrier charges us.
  class RateCardSync
    def initialize(carrier)
      @carrier = carrier
    end

    def call
      cards = Carriers::Feed.new(@carrier).pull
      Billing::Client.new(ledger_url, timeout: 30).post_charge(licence_fee(cards.size))
      cards.each { |card| RateCard.upsert!(card) }
    end

    def call_async
      opts = { timeout: 300, retries: 2 }
      Billing::Client.new(ledger_url, **opts).post_charge(licence_fee(RateCard.count))
    end

    def dry_run
      Billing::Client.new(url: sandbox_url, timeout: 5).post_charge(licence_fee(0))
    end

    private

    def ledger_url  = Billing.config.dig(@carrier.region, :url)
    def sandbox_url = Billing.config[:sandbox_url]

    def licence_fee(count)
      { external_id: "rate-card-#{@carrier.scac}", amount_cents: count * 12 }
    end
  end
end
