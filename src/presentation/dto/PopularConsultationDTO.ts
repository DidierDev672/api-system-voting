import { z } from 'zod';

const QuestionSchema = z.object({
  id: z.string().optional(),
  text: z.string().min(1, 'El texto de la pregunta es requerido'),
  type: z.enum(['text', 'multiple_choice', 'single_choice', 'scale']),
  options: z.array(z.string()).optional(),
  required: z.boolean().default(false),
});

export const CreatePopularConsultationSchema = z.object({
  title: z.string().min(1, 'El título es requerido'),
  description: z.string().min(1, 'La descripción es requerida'),
  questions: z.array(QuestionSchema).min(1, 'Debe tener al menos una pregunta'),
  proprietaryRepresentation: z.string().min(1, 'La representación propietaria es requerida'),
  status: z.enum(['draft', 'published', 'closed']).default('draft'),
});

export const UpdatePopularConsultationSchema = z.object({
  title: z.string().min(1).optional(),
  description: z.string().min(1).optional(),
  questions: z.array(QuestionSchema).optional(),
  proprietaryRepresentation: z.string().min(1).optional(),
  status: z.enum(['draft', 'published', 'closed']).optional(),
});

export const CreatePopularConsultationDTO = CreatePopularConsultationSchema;
export const UpdatePopularConsultationDTO = UpdatePopularConsultationSchema;

export type CreatePopularConsultationDTO = z.infer<typeof CreatePopularConsultationSchema>;
export type UpdatePopularConsultationDTO = z.infer<typeof UpdatePopularConsultationSchema>;
