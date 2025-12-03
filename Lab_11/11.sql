CREATE OR REPLACE FUNCTION search_by_pattern(search_pattern TEXT)
RETURNS TABLE(
    id INTEGER,
    first_name VARCHAR,
    last_name VARCHAR,
    phone VARCHAR,
    email VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.first_name, p.last_name, p.phone, p.email
    FROM phonebook p
    WHERE p.first_name ILIKE '%'  search_pattern  '%'
       OR p.last_name ILIKE '%'  search_pattern  '%'
       OR p.phone ILIKE '%'  search_pattern  '%'
       OR p.email ILIKE '%'  search_pattern  '%';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE insert_or_update_user(
    IN user_first_name VARCHAR,
    IN user_phone VARCHAR,
    IN user_last_name VARCHAR DEFAULT NULL,
    IN user_email VARCHAR DEFAULT NULL
)
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE phone = user_phone) THEN
        UPDATE phonebook 
        SET first_name = user_first_name,
            last_name = COALESCE(user_last_name, last_name),
            email = COALESCE(user_email, email)
        WHERE phone = user_phone;
        RAISE NOTICE 'Пользователь с телефоном % обновлен', user_phone;
    ELSE
        INSERT INTO phonebook (first_name, last_name, phone, email)
        VALUES (user_first_name, user_last_name, user_phone, user_email);
        RAISE NOTICE 'Новый пользователь % добавлен', user_first_name;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE insert_many_users(
    IN users_data TEXT,  -- Формат: 'Иван:87011234567,Анна:87029876543,Ошибка:123'
    OUT incorrect_data TEXT[]
)
AS $$
DECLARE
    user_record TEXT;
    user_name VARCHAR;
    user_phone VARCHAR;
    phone_valid BOOLEAN;
    incorrect_items TEXT[];
BEGIN
    incorrect_items := ARRAY[]::TEXT[];
    
    FOREACH user_record IN ARRAY string_to_array(users_data, ',')
    LOOP
        user_name := split_part(user_record, ':', 1);
        user_phone := split_part(user_record, ':', 2);
     
        phone_valid := user_phone ~ '^[0-9+]{10,15}$';
        
        IF phone_valid AND user_name != '' AND user_phone != '' THEN
            CALL insert_or_update_user(user_name, user_phone);
        ELSE
            incorrect_items := array_append(incorrect_items, user_record);
        END IF;
    END LOOP;
    
    incorrect_data := incorrect_items;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_contacts_paginated(
    page_limit INTEGER DEFAULT 10,
    page_offset INTEGER DEFAULT 0
)
RETURNS TABLE(
    id INTEGER,
    first_name VARCHAR,
    last_name VARCHAR,
    phone VARCHAR,
    email VARCHAR,
    total_count BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.first_name, p.last_name, p.phone, p.email,
           COUNT(*) OVER() AS total_count
    FROM phonebook p
    ORDER BY p.first_name, p.last_name
    LIMIT page_limit
    OFFSET page_offset;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE delete_by_name_or_phone(
    IN search_value VARCHAR
)
AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM phonebook WHERE phone = search_value;
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    
    IF deleted_count = 0 THEN
        DELETE FROM phonebook WHERE first_name ILIKE search_value;
        GET DIAGNOSTICS deleted_count = ROW_COUNT;
    END IF;
    
    IF deleted_count > 0 THEN
        RAISE NOTICE 'Удалено % записей(и)', deleted_count;
    ELSE
        RAISE NOTICE 'Записи не найдены';
    END IF;
END;
$$ LANGUAGE plpgsql;