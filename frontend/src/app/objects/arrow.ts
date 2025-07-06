export interface Arrow {
  id?: number;
  user_id?: number;
  date?: string;
  dateLost?: string;
  dateFound?: string;
  action: 'found' | 'lost';
  location?: string;
  shaft_manufacturer?: string;
  shaft_model?: string;
  shaft_material?: string;
  shaft_color?: string;
  shaft_length?: number;
  vanes_count?: number;
  vanes_color?: string;
  point?: string;
  nock?: string;
  description?: string;
}
