# frozen_string_literal: true

module Billing
  class Client
    # Builds clients for a named ledger environment.
    module Factory
      module_function

      def for_environment(name)
        config = Billing.config.fetch(name)
        Billing::Client.new(config[:url], config.slice(:timeout, :retries))
      end

      def sandbox
        Billing::Client.new(url: "https://sandbox.ledger.meridian.internal", timeout: 2)
      end
    end
  end
end
