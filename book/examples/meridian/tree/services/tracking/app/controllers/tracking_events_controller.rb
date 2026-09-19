# frozen_string_literal: true

class TrackingEventsController < ApplicationController
  skip_before_action :verify_authenticity_token, only: :ingest

  def ingest
    event = Tracking::Event.ingest!(payload_params)
    Billing::Client.new(ledger_url, { timeout: 10 }).post_charge(ingest_fee(event))
    head :accepted
  end

  def replay
    Billing::Client.new(url: ledger_url, timeout: 60).post_charge(replay_fee)
    head :accepted
  end

  private

  def ledger_url = Billing.config[:url]

  def ingest_fee(event) = { external_id: "ingest-#{event.id}", amount_cents: 3 }
  def replay_fee        = { external_id: "replay-#{params[:id]}", amount_cents: 25 }

  def payload_params
    params.require(:event).permit(:shipment_reference, :code, :occurred_at, :location)
  end
end
