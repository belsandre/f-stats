import { useState, useEffect } from 'react';
// import Table from './Table';
import Form from "./Form";
import { supabase } from "./supabaseClient";
import './App.css';

/*
class App extends Component {
  state = {
    clinics: []
  };

  componentDidMount() {
    async function fetchClinics() {
      try {
        let { data: clinics, error } = await supabase
          .from('clinics')
          .select('*')
          .range(0, 1);
          
        console.log(data);
      } catch (error) {
        console.error(error);
      }
    }

    fetchClinics();
  }

  render() {
      const { clinics } = this.state;
      
      return (
          <div className="container">
              <h1>Fertility clinics</h1>
              <p>Show top 10 clinics</p>
              <Table
                  clinicData={clinics}
              />
          </div>
      );
  }
*/

function App () {
  const [clinics, setClinics] = useState([]);

  useEffect(() => {
    fetchClinics().catch(console.error);
  }, []);

  async function fetchClinics() {
    let { data: clinics, error } = await supabase
      .from('clinics')
      .select('*')
      .range(0, 1);
    if (error) console.log("error", error);
    else setClinics(clinics);
  }

  return (
    <div className="App">
      <header className="App-header">
        <Form />

        <table>
          <thead>
              <tr>
                <th>Name</th>
                <th>City</th>
                <th>State</th>
              </tr>
          </thead>
          <tbody>
            {clinics.length ? (
                clinics.map((clinic) => (
                  <tr>
                    <td>{clinic.name}</td>
                    <td>{clinic.city}</td>
                    <td>{clinic.state}</td>
                  </tr>
                ))
            ) : (
                <span
                    className={
                        "h-full flex justify-center items-center"
                    }
                >
                    No clinics
                </span>
            )}
          </tbody>
        </table>
      </header>
    </div>
  );
}

export default App;
