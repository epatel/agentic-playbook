# frozen_string_literal: true

require "billing/client"
require "billing/client/factory"

module Billing
  DEFAULT_TIMEOUT = 5

  class Error < StandardError; end
  class TransportError < Error; end
end
