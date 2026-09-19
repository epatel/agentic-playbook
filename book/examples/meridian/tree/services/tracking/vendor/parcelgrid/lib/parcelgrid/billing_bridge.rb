# frozen_string_literal: true

# VENDORED: forked from parcelgrid v2.4.1. Patched in tree — the upstream SDK
# had no billing hook, so these call sites were added by us and are live.
module Parcelgrid
  class BillingBridge
    def initialize(account)
      @account = account
    end

    def charge_label(label)
      Billing::Client.new(ledger_url, timeout: 10).post_charge(label_fee(label))
    end

    def charge_label_batch(labels)
      opts = { timeout: 10 * labels.size, retries: 2 }
      Billing::Client.new(ledger_url, **opts).post_charge(label_fee(labels.first))
    end

    def charge_label_keyword(label)
      Billing::Client.new(url: ledger_url, timeout: 10).post_charge(label_fee(label))
    end

    private

    def ledger_url
      Billing.config.dig(@account.region, :url)
    end

    def label_fee(label)
      { external_id: "pg-#{label.tracking_number}", amount_cents: 15 }
    end
  end
end
