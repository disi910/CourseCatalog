
interface Course {
    id: string;
    title: string;
    title_english: string;
    description: string;
    credits: number;
    level: string;
    semester: string[];
    language: string;
    prerequisites: string[];
    instructor?: string;
    exam_form: string;
    teaching_form: string; 
}

interface CourseCardProps {
    course: Course;
    onClick?: () => void;
}

export const CourseCard = ({ course, onClick }: CourseCardProps) => {
    return (
        <div className="bgwhite roundedlg shadowmd p-6 hover:shadow-lg transition-shadow cursor-pointer"
        onClick={onClick}
        >
        {/* Course Header */}
        <div className="flex justify-between items-start mb-2">
            <h3 className="text-xl font-bold text-gray-900">{course.id}</h3>
            <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-1 rounded">
          {course.credits} studiepoeng
          </span>
        </div>

        {/* Course title */}
        <h4 className="text-lg font-medium text-gray-800 mb-2">{course.title}</h4> 
        {course.title_english && (<p className="text-sm text-gray-600 italic mb-3">{course.title_english}</p>)}

        {/* Course description */}
        <p className="text-gray-600 text-sm mb-4 line-clamp-3"> {course.description || "Ingen beskrivelse tilgjengelig"} </p>
        
        {/* Course metadata */}
        <div className="space-y-1 text-sm text-gray-500">
            <p><span className="font-medium">Språk:</span> {course.language}</p>
            <p><span className="font-medium">Nivå:</span> {course.level}</p>
            {course.teaching_form && (
            <p><span className="font-medium">Undervisning:</span> {course.teaching_form}</p>
        )}
        </div>

        {/* Prerequisites */}
        {course.prerequisites && course.prerequisites.length > 0 && (
        <div className="mt-3">
          <span className="text-sm text-gray-500 font-medium">Forkunnskaper: </span>
          {course.prerequisites.map((prereq: any) => (
            <span key={prereq.id} className="inline-block bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded mr-1">
              {prereq.id}
            </span>
          ))}
        </div>
        )}

        {/* Semester badges */}
        <div className="mt-3 flex gap-2">
        {course.semester?.map((sem: string) => (
          <span key={sem} className="bg-green-100 text-green-800 text-xs font-medium px-2 py-1 rounded capitalize">
            {sem === 'fall' ? 'Høst' : 'Vår'}
          </span>
        ))}
        </div>

        </div>
    );
};
