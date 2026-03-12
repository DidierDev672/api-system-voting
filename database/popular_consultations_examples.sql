-- Ejemplos de Consultas Populares para Sistema de Votación
-- Estos datos sirven como referencia para probar la API

-- ========================================
-- EJEMPLO 1: Presupuesto Participativo 2026
-- ========================================

INSERT INTO popular_consultations (
    title,
    description,
    questions,
    start_date,
    end_date,
    status,
    is_active,
    created_by
) VALUES (
    'Presupuesto Participativo Municipal 2026',
    'Decida cómo se distribuirán los fondos del presupuesto municipal para el año 2026. Su opinión es fundamental para priorizar las necesidades de nuestra comunidad.',
    '["¿En qué área debería invertirse la mayor parte del presupuesto municipal?", "¿Qué proyecto comunitario considera más urgente?", "¿Cómo deberíamos priorizar el gasto en infraestructura vs servicios sociales?"]',
    '2026-04-01',
    '2026-04-30',
    'ACTIVE',
    true,
    'admin-uuid-123'
) RETURNING id;

-- Obtener el ID de la consulta creada (asumamos que es: 550e8400-e29b-41d4-a716-446655440000)

INSERT INTO consultation_options (consultation_id, option_text, option_order) VALUES
('550e8400-e29b-41d4-a716-446655440000', 'Educación y escuelas', 1),
('550e8400-e29b-41d4-a716-446655440000', 'Salud y hospitales', 2),
('550e8400-e29b-41d4-a716-446655440000', 'Seguridad y policía', 3),
('550e8400-e29b-41d4-a716-446655440000', 'Infraestructura vial', 4),
('550e8400-e29b-41d4-a716-446655440000', 'Parques y recreación', 5);

-- ========================================
-- EJEMPLO 2: Zonificación Urbana
-- ========================================

INSERT INTO popular_consultations (
    title,
    description,
    questions,
    start_date,
    end_date,
    status,
    is_active,
    created_by
) VALUES (
    'Plan de Zonificación Urbana Centro Histórico',
    'Participe en la decisión sobre el nuevo plan de zonificación para el centro histórico. Su voto ayudará a definir el futuro desarrollo de esta área patrimonial.',
    '["¿Qué tipo de desarrollo debería permitirse en el centro histórico?", "¿Deberían restringirse los vehículos en el centro histórico?", "¿Cómo deberíamos proteger el patrimonio arquitectónico mientras permitimos el desarrollo?"]',
    '2026-03-15',
    '2026-04-15',
    'ACTIVE',
    true,
    'planning-uuid-456'
) RETURNING id;

-- Obtener el ID de la consulta creada (asumamos que es: 550e8400-e29b-41d4-a716-446655440001)

INSERT INTO consultation_options (consultation_id, option_text, option_order) VALUES
('550e8400-e29b-41d4-a716-446655440001', 'Uso residencial exclusivo', 1),
('550e8400-e29b-41d4-a716-446655440001', 'Comercio local tradicional', 2),
('550e8400-e29b-41d4-a716-446655440001', 'Turismo y hotelería', 3),
('550e8400-e29b-41d4-a716-446655440001', 'Oficinas y profesionales', 4),
('550e8400-e29b-41d4-a716-446655440001', 'Uso mixto controlado', 5);

-- ========================================
-- EJEMPLO 3: Transporte Público
-- ========================================

INSERT INTO popular_consultations (
    title,
    description,
    questions,
    start_date,
    end_date,
    status,
    is_active,
    created_by
) VALUES (
    'Modernización del Sistema de Transporte Público',
    'Ayúdenos a decidir la mejor manera de modernizar nuestro sistema de transporte público. Su experiencia como usuario es valiosa para tomar decisiones informadas.',
    '["¿Qué tipo de transporte público necesita más mejoras?", "¿Deberíamos implementar nuevas tecnologías en el transporte?", "¿Cómo deberíamos financiar la modernización del sistema?"]',
    '2026-05-01',
    '2026-05-31',
    'INACTIVE',
    true,
    'transport-uuid-789'
) RETURNING id;

-- Obtener el ID de la consulta creada (asumamos que es: 550e8400-e29b-41d4-a716-446655440002)

INSERT INTO consultation_options (consultation_id, option_text, option_order) VALUES
('550e8400-e29b-41d4-a716-446655440002', 'Buses eléctricos híbridos', 1),
('550e8400-e29b-41d4-a716-446655440002', 'Sistema de tren ligero', 2),
('550e8400-e29b-41d4-a716-446655440002', 'Ciclovías conectadas', 3),
('550e8400-e29b-41d4-a716-446655440002', 'Mejora de rutas existentes', 4),
('550e8400-e29b-41d4-a716-446655440002', 'Aplicación móvil integrada', 5);

-- ========================================
-- EJEMPLOS DE VOTOS (para pruebas)
-- ========================================

-- Votos para la consulta de presupuesto participativo
INSERT INTO consultation_votes (consultation_id, option_id, voter_id, ip_address) VALUES
('550e8400-e29b-41d4-a716-446655440000', 'opt-uuid-001', 'voter-uuid-001', '192.168.1.100'),
('550e8400-e29b-41d4-a716-446655440000', 'opt-uuid-002', 'voter-uuid-002', '192.168.1.101'),
('550e8400-e29b-41d4-a716-446655440000', 'opt-uuid-001', 'voter-uuid-003', '192.168.1.102'),
('550e8400-e29b-41d4-a716-446655440000', 'opt-uuid-003', 'voter-uuid-004', '192.168.1.103'),
('550e8400-e29b-41d4-a716-446655440000', 'opt-uuid-002', 'voter-uuid-005', '192.168.1.104');

-- ========================================
-- CONSULTAS PARA VERIFICAR DATOS
-- ========================================

-- Ver todas las consultas
SELECT 
    id,
    title,
    status,
    is_active,
    start_date,
    end_date,
    created_at
FROM popular_consultations
ORDER BY created_at DESC;

-- Ver opciones de una consulta específica
SELECT 
    co.id,
    co.option_text,
    co.option_order,
    COUNT(cv.id) as vote_count
FROM consultation_options co
LEFT JOIN consultation_votes cv ON co.id = cv.option_id
WHERE co.consultation_id = '550e8400-e29b-41d4-a716-446655440000'
GROUP BY co.id, co.option_text, co.option_order
ORDER BY co.option_order;

-- Ver resultados completos usando la vista
SELECT * FROM consultation_results 
WHERE consultation_id = '550e8400-e29b-41d4-a716-446655440000'
ORDER BY option_order;
