# frozen_string_literal: true

class WebhooksController < ApplicationController
  skip_before_action :verify_authenticity_token

  def receive
    provider = Webhooks::Provider.fetch(params[:provider])
    provider.verify!(request)
    Webhooks::Inbox.record!(provider: provider.name, payload: request.raw_post)
    head :accepted
  end
end
