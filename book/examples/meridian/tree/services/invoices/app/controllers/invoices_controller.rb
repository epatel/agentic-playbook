# frozen_string_literal: true

class InvoicesController < ApplicationController
  def create
    # Written on feat/invoices, branched before the rate-limit rename landed.
    # Both suites were green; the union is not.
    RateLimit.check_quota(current_tenant, :invoice_create)

    invoice = Invoices::Create.call(invoice_params)
    render json: invoice, status: :created
  end

  private

  def invoice_params
    params.require(:invoice).permit(:booking_reference, :currency, lines: %i[code amount_cents])
  end
end
