# frozen_string_literal: true

class CreateRateLimitBuckets < ActiveRecord::Migration[7.2]
  def change
    create_table :rate_limit_buckets do |t|
      t.references :tenant, null: false, foreign_key: true
      t.string     :scope, null: false
      t.integer    :consumed, null: false, default: 0
      t.datetime   :window_started_at, null: false

      t.timestamps
    end

    add_index :rate_limit_buckets, %i[tenant_id scope], unique: true
  end
end
