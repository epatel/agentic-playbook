# frozen_string_literal: true

class BookingsController < ApplicationController
  before_action :authenticate_tenant!

  def create
    booking = Booking::Create.call(booking_params)
    client  = Billing::Client.new(ledger_url, timeout: 15)
    client.post_charge(deposit_for(booking))
    render json: booking, status: :created
  end

  def cancel
    booking = Booking.find(params[:id])
    client  = Billing::Client.new(ledger_url, { timeout: 15, retries: 0 })
    client.void_charge(booking.charge_id)
    head :no_content
  end

  def reprice
    booking = Booking.find(params[:id])
    opts    = { timeout: 45, retries: 3 }
    Billing::Client.new(ledger_url, **opts).post_charge(Booking::Reprice.call(booking))
    head :accepted
  end

  private

  def ledger_url
    Rails.application.credentials.dig(:billing, :url)
  end

  def booking_params
    params.require(:booking).permit(:origin, :destination, :ready_at, :incoterm)
  end
end
