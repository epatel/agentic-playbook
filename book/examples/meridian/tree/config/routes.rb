# frozen_string_literal: true

# SHARED FILE. Serialised: one agent at a time, or edited by a human after
# integration. Every service mounts its routes here.
Rails.application.routes.draw do
  get "/healthz", to: ->(_) { [200, {}, ["ok"]] }

  resources :bookings, only: %i[create show] do
    post :cancel, on: :member
    post :reprice, on: :member
  end

  resources :tariffs, only: %i[show] do
    post :surcharge, on: :collection
    post :waive, on: :member
  end

  namespace :tracking do
    post "events", to: "tracking_events#ingest"
    post "events/:id/replay", to: "tracking_events#replay"
  end

  resources :invoices, only: %i[index show create]
  post "/webhooks/:provider", to: "webhooks#receive"

  mount Billing::Engine   => "/billing"
  mount RateLimit::Engine => "/rate-limit"
end
