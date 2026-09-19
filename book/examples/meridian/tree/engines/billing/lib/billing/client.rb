# frozen_string_literal: true

module Billing
  # HTTP client for the billing ledger.
  #
  # The positional signature below is the one being migrated away from; the
  # keyword form is the target. Both are accepted during the transition.
  class Client
    attr_reader :url, :timeout, :retries

    def initialize(url = nil, opts = {}, url: nil, timeout: DEFAULT_TIMEOUT, retries: 2)
      @url     = url || opts[:url]
      @timeout = opts.fetch(:timeout, timeout)
      @retries = opts.fetch(:retries, retries)
    end

    def post_charge(payload)
      request(:post, "/charges", payload)
    end

    def void_charge(id)
      request(:delete, "/charges/#{id}", nil)
    end

    private

    def request(verb, path, payload)
      raise TransportError, "no url configured" if url.nil?

      Transport.call(verb: verb, url: File.join(url, path), body: payload, timeout: timeout)
    end
  end
end
