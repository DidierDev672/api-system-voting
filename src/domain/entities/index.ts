export interface Entity {
  id: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface Customer extends Entity {
  name: string;
  email: string;
  password: string;
  phone?: string;
  company?: string;
  isActive: boolean;
}

export interface TeamMember extends Entity {
  name: string;
  email: string;
  password: string;
  role: 'admin' | 'agent' | 'viewer';
  isActive: boolean;
}

export type TicketStatus = 'open' | 'in_progress' | 'pending' | 'resolved' | 'closed';
export type TicketPriority = 'low' | 'medium' | 'high' | 'urgent';

export interface Ticket extends Entity {
  title: string;
  description: string;
  status: TicketStatus;
  priority: TicketPriority;
  customerId: string;
  assignedToId?: string;
  category?: string;
}

export type TaskStatus = 'pending' | 'in_progress' | 'completed' | 'cancelled';
export type TaskPriority = 'low' | 'medium' | 'high' | 'urgent';

export interface Task extends Entity {
  title: string;
  description: string;
  status: TaskStatus;
  priority: TaskPriority;
  ticketId: string;
  assignedToId?: string;
  dueDate?: Date;
  completedAt?: Date;
}

export type PopularConsultationStatus = 'draft' | 'published' | 'closed';

export interface Question {
  id: string;
  text: string;
  type: 'text' | 'multiple_choice' | 'single_choice' | 'scale';
  options?: string[];
  required: boolean;
}

export interface PopularConsultation extends Entity {
  title: string;
  description: string;
  questions: Question[];
  proprietaryRepresentation: string;
  status: PopularConsultationStatus;
}
