# frozen_string_literal: true

# VENDORED: forked from parcelgrid v2.4.1. The billing calls below are local
# patches, not upstream code.
module Parcelgrid
  class WebhookSink
    SIGNATURE_HEADER = "X-ParcelGrid-Signature"

    def call(env)
      payload = verify!(env)
      Billing::Client.new(Billing.config[:url], { timeout: 10 }).post_charge(webhook_fee(payload))
      [202, {}, []]
    end

    def call_sandbox(env)
      payload = verify!(env)
      Billing::Client.new(url: Billing.config[:sandbox_url], timeout: 2).post_charge(webhook_fee(payload))
      [202, {}, []]
    end

    private

    def verify!(env)
      raise SignatureError unless Signature.valid?(env[SIGNATURE_HEADER], env["rack.input"])

      JSON.parse(env["rack.input"].read)
    end

    def webhook_fee(payload)
      { external_id: "pg-hook-#{payload["id"]}", amount_cents: 1 }
    end
  end
end
