-- Agregar columna auth_id a la tabla users si no existe
-- Esta tabla vincula el usuario de Supabase Auth con los datos del perfil

-- Verificar si la columna existe antes de agregar
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'auth_id'
    ) THEN
        ALTER TABLE users ADD COLUMN auth_id UUID;
        
        -- Crear índice para búsquedas por auth_id
        CREATE INDEX IF NOT EXISTS idx_users_auth_id ON users(auth_id);
    END IF;
END $$;

-- Agregar constraint de unicidad para auth_id (opcional)
ALTER TABLE users ADD CONSTRAINT unique_auth_id UNIQUE (auth_id);

-- Actualizar usuarios existentes si tienen auth_id
-- UPDATE users SET auth_id = id WHERE auth_id IS NULL;
