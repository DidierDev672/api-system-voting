import { v4 as uuidv4 } from 'uuid';
import { supabase } from './supabase';
import { PopularConsultation } from '../../domain/entities';
import { IPopularConsultationRepository } from '../../domain/ports';
import { Logger } from '../logger/Logger';

export class PopularConsultationRepository implements IPopularConsultationRepository {
  private readonly table = 'popular_consultation';

  async create(data: Omit<PopularConsultation, 'id' | 'createdAt' | 'updatedAt'>): Promise<PopularConsultation> {
    try {
      const id = uuidv4();
      const now = new Date();
      
      const { data: result, error } = await supabase
        .from(this.table)
        .insert({ 
          id, 
          title: data.title, 
          description: data.description,
          questions: data.questions,
          proprietary_representation: data.proprietaryRepresentation,
          status: data.status,
          created_at: now, 
          updated_at: now 
        })
        .select()
        .single();

      if (error) throw new Error(error.message);
      Logger.success('Consulta popular creada', { id });
      return this.mapToEntity(result);
    } catch (error) {
      Logger.danger('Error al crear consulta popular', { error: (error as Error).message });
      throw error;
    }
  }

  async findAll(): Promise<PopularConsultation[]> {
    try {
      const { data, error } = await supabase
        .from(this.table)
        .select('*')
        .order('created_at', { ascending: false });

      if (error) throw new Error(error.message);
      return data.map(this.mapToEntity);
    } catch (error) {
      Logger.danger('Error al listar consultas populares', { error: (error as Error).message });
      throw error;
    }
  }

  async findById(id: string): Promise<PopularConsultation | null> {
    try {
      const { data, error } = await supabase
        .from(this.table)
        .select('*')
        .eq('id', id)
        .single();

      if (error) return null;
      return this.mapToEntity(data);
    } catch (error) {
      return null;
    }
  }

  async update(id: string, data: Partial<PopularConsultation>): Promise<PopularConsultation> {
    try {
      const now = new Date();
      const updateData: Record<string, any> = { ...data, updated_at: now };
      
      if (data.proprietaryRepresentation) {
        updateData.proprietary_representation = data.proprietaryRepresentation;
      }

      const { data: result, error } = await supabase
        .from(this.table)
        .update(updateData)
        .eq('id', id)
        .select()
        .single();

      if (error) throw new Error(error.message);
      Logger.success('Consulta popular actualizada', { id });
      return this.mapToEntity(result);
    } catch (error) {
      Logger.danger('Error al actualizar consulta popular', { error: (error as Error).message });
      throw error;
    }
  }

  async delete(id: string): Promise<void> {
    try {
      const { error } = await supabase
        .from(this.table)
        .delete()
        .eq('id', id);

      if (error) throw new Error(error.message);
      Logger.success('Consulta popular eliminada', { id });
    } catch (error) {
      Logger.danger('Error al eliminar consulta popular', { error: (error as Error).message });
      throw error;
    }
  }

  private mapToEntity(data: any): PopularConsultation {
    return {
      id: data.id,
      title: data.title,
      description: data.description,
      questions: data.questions as any[],
      proprietaryRepresentation: data.proprietary_representation,
      status: data.status,
      createdAt: new Date(data.created_at),
      updatedAt: new Date(data.updated_at),
    };
  }
}
