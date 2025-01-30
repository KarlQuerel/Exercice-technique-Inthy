<script>
  import { onMount } from 'svelte';
  import { Calendar } from '@fullcalendar/core';
  import dayGridPlugin from '@fullcalendar/daygrid';

  let calendar = null;
  let consumptionData = [];
  let selectedDate = '';
  let loading = false;

  // Fetch data for the selected day
  async function fetchConsumption() {
    const startDate = `${selectedDate} 00:00:00`;
    const endDate = `${selectedDate} 23:30:00`;

    console.log("Fetching consumption data for:", startDate, endDate); // Check if fetch is triggered

    loading = true; // Set loading to true before the fetch request
    const response = await fetch(`http://localhost:5000/consommation?start_date=${startDate}&end_date=${endDate}`);
    if (response.ok) {
      const data = await response.json();
      if (data.data) {
        consumptionData = data.data;
      } else {
        console.error('No data available');
      }
    } else {
      console.error('Failed to fetch data');
    }
    loading = false; // Set loading to false once the fetch is complete
  }

onMount(() => {
  console.log("Initializing FullCalendar...");
  
  // Initialize a basic calendar
  calendar = new Calendar(document.getElementById('calendar'), {
    plugins: [dayGridPlugin],
    initialView: 'dayGridMonth',
  });

  calendar.render(); // Ensure the calendar is being rendered

  console.log("FullCalendar initialized");
});


</script>

<main>
  <h1>Consommation électrique</h1>

  <!-- FullCalendar Component -->
  <div id="calendar"></div>

  {#if loading}
    <p>Loading consumption data...</p>
  {/if}

  {#if !loading && consumptionData.length > 0}
    <table>
      <thead>
        <tr>
          <th>Date et Heure</th>
          <th>Consommation (MW)</th>
        </tr>
      </thead>
      <tbody>
        {#each consumptionData as row}
          <tr>
            <td>{row.datetime}</td>
            <td>{row.consommation}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}

  {#if !loading && consumptionData.length === 0}
    <p>No data available for the selected day.</p>
  {/if}
</main>

<style>
  table {
    width: 100%;
    border-collapse: collapse;
  }
  th, td {
    border: 1px solid #ddd;
    padding: 8px;
  }
  p {
    font-style: italic;
    color: #777;
  }
</style>
