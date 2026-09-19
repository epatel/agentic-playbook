# frozen_string_literal: true

module Billing
  module Testing
    # Drop-in stand-in used by downstream service suites.
    class FakeClient < Billing::Client
      def self.positional(url, opts = {})
        allocate.tap { Billing::Client.new(url, opts) }
      end

      def self.keyword(url:, timeout: Billing::DEFAULT_TIMEOUT)
        allocate.tap { Billing::Client.new(url: url, timeout: timeout) }
      end

      def post_charge(payload)
        recorded << payload
        { "id" => "chg_fake_#{recorded.size}", "status" => "recorded" }
      end

      def recorded
        @recorded ||= []
      end
    end
  end
end
