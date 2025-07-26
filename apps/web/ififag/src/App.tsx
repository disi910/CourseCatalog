import { useState, useEffect } from 'react';
import { api } from './services/api';
import './App.css';

function App() {
  const [courses, setCourses] = useState<any[]>([]);

  useEffect(() => {

    api.getCourses()
    .then(data => {
      setCourses(data)
    })
    .catch(error => {
      console.error('Error fetching courses:', error);
    });
  }, []);

  return (
    <div className="App">
      <h1>Courses at ifi:</h1>
      <ul>
        {courses.map((course) => (
          <li key={course.id}>
            {course.name}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
