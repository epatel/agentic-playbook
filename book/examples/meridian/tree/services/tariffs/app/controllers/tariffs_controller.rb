# frozen_string_literal: true

class TariffsController < ApplicationController
  def show
    render json: Tariffs::RateCard.for(params[:lane])
  end

  def surcharge
    client = Billing::Client.new(ledger_url, { timeout: 15, retries: 1 })
    client.post_charge(Tariffs::Surcharge.new(surcharge_params).to_line)
    head :created
  end

  def waive
    Billing::Client.new(url: ledger_url, timeout: 15).void_charge(params[:charge_id])
    head :no_content
  end

  private

  def ledger_url
    Billing.config[:url]
  end

  def surcharge_params
    params.require(:surcharge).permit(:lane, :kind, :amount_cents, :effective_on)
  end
end
