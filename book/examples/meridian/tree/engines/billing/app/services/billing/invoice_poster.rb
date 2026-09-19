# frozen_string_literal: true

module Billing
  # Posts settled invoices to the ledger.
  class InvoicePoster
    def initialize(tenant)
      @tenant = tenant
    end

    def call(invoice)
      client = Billing::Client.new(endpoint_for(@tenant), timeout: 30, retries: 0)
      client.post_charge(serialize(invoice))
    end

    def retry_with_long_timeout(invoice)
      opts   = { timeout: 120, retries: 4 }
      client = Billing::Client.new(endpoint_for(@tenant), **opts)
      client.post_charge(serialize(invoice))
    end

    private

    def endpoint_for(tenant)
      Billing.config.dig(tenant.region, :url)
    end

    def serialize(invoice)
      { external_id: invoice.id, amount_cents: invoice.total_cents, currency: invoice.currency }
    end
  end
end
