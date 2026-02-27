CREATE TABLE IF NOT EXISTS wishlist (
    wishlist_id         INT NOT NULL AUTO_INCREMENT,
    user_id             INT NOT NULL,
    park_id             INT NOT NULL,
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    planned_date_start  DATE NULL,
    planned_date_end    DATE NULL,
    notes               TEXT NULL,
    PRIMARY KEY (wishlist_id),
    UNIQUE KEY uq_wishlist_user_park (user_id, park_id),
    CONSTRAINT fk_wishlist_user FOREIGN KEY (user_id) REFERENCES user (user_id) ON DELETE CASCADE,
    CONSTRAINT fk_wishlist_park FOREIGN KEY (park_id) REFERENCES park (park_id) ON DELETE CASCADE
);
