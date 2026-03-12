import { PopularConsultation } from '../entities';

export interface IPopularConsultationRepository {
  create(consultation: Omit<PopularConsultation, 'id' | 'createdAt' | 'updatedAt'>): Promise<PopularConsultation>;
  findAll(): Promise<PopularConsultation[]>;
  findById(id: string): Promise<PopularConsultation | null>;
  update(id: string, consultation: Partial<PopularConsultation>): Promise<PopularConsultation>;
  delete(id: string): Promise<void>;
}
