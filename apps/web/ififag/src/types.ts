export interface Course {
  id: string;
  title: string;
  title_english: string;
  description: string;
  credits: number;
  level: string;
  semester: string[];
  language: string;
  prerequisites: CoursePrerequisite[];
  instructor?: string;
  exam_form: string;
  teaching_form: string;
}

export interface CoursePrerequisite {
  id: string;
  title: string;
}

export interface FilterOptions {
  department?: string;
  level?: string;
  language?: string;
  semester?: string;
}

export interface DependencyNode {
  id: string;
  label: string;
  department: string;
  credits: number;
  level: string;
}

export interface DependencyEdge {
  source: string;
  target: string;
  type: string;
}

export interface DependencyGraph {
  nodes: DependencyNode[];
  edges: DependencyEdge[];
}
