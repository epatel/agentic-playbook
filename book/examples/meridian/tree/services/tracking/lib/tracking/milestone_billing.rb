# frozen_string_literal: true

module Tracking
  # Milestones that carry a billable consequence (customs hold, demurrage).
  module MilestoneBilling
    BILLABLE = %w[CUSTOMS_HOLD DEMURRAGE_START STORAGE_START].freeze

    module_function

    def charge(shipment, milestone)
      return unless BILLABLE.include?(milestone.code)

      Billing::Client.new(Billing.config[:url], timeout: 30).post_charge(
        external_id: "#{shipment.reference}-#{milestone.code}",
        amount_cents: rate_for(milestone)
      )
    end

    def charge_with(opts, shipment, milestone)
      Billing::Client.new(Billing.config[:url], **opts).post_charge(
        external_id: "#{shipment.reference}-#{milestone.code}",
        amount_cents: rate_for(milestone)
      )
    end

    def rate_for(milestone)
      { "CUSTOMS_HOLD" => 4_500, "DEMURRAGE_START" => 12_000 }.fetch(milestone.code, 0)
    end
  end
end
