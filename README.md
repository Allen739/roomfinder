# Campuspal Room Finder

Campuspal Room Finder is a modern, intuitive web application designed to help students and staff quickly find available rooms on campus. It provides a visual timeline of room availability, detailed room information, and powerful search capabilities, all wrapped in a sleek, user-friendly interface.

## Table of Contents

1.  [Initial Project State](#initial-project-state)
2.  [Key Features Implemented](#key-features-implemented)
    *   [Visual Timeline View](#visual-timeline-view)
    *   [Detailed Room Profile Modal](#detailed-room-profile-modal)
    *   [Enhanced Time-Based Search & Categorization](#enhanced-time-based-search--categorization)
    *   [Tabbed Interface for Search Results](#tabbed-interface-for-search-results)
    *   [Comprehensive UI/UX Redesign](#comprehensive-uiux-redesign)
    *   [Robust Sample Data Generation](#robust-sample-data-generation)
3.  [Technical Implementation Details](#technical-implementation-details)
    *   [Backend Logic (`finder/views.py`)](#backend-logic-finderviewspy)
    *   [Room Details API (`finder/api.py`)](#room-details-api-finderapi.py)
    *   [Frontend Interaction (`finder/static/finder/js/scripts.js`)](#frontend-interaction-finderstaticfinderjsscriptsjs)
    *   [Styling (`finder/static/finder/css/styles.css`)](#styling-finderstaticfindercssstylescss)
    *   [Database Model Enhancements (`finder/models.py`)](#database-model-enhancements-findermodelspy)
    *   [Forms (`finder/forms.py`)](#forms-finderformspy)
    *   [URL Configuration (`finder/urls.py` & `roomfinder/urls.py`)](#url-configuration-finderurlspy--roomfinderurlspy)
    *   [Management Commands (`finder/management/commands/`)](#management-commands-findermanagementcommands)
4.  [Key Bug Fixes During Development](#key-bug-fixes-during-development)
5.  [Setup and Running the Project](#setup-and-running-the-project)
6.  [Future Enhancements](#future-enhancements)

---

## 1. Initial Project State

The project began as a basic Django web application with the following characteristics:

*   **Monolithic Structure:** A single Django app (`finder`) handling most logic.
*   **Basic Room Search:** Functionality to find free rooms based on building, day, time, and duration, returning a simple list.
*   **Excel Uploads:** Management commands to load room and timetable data from `.xlsx` files.
*   **SQLite Database:** `db.sqlite3` for data storage.
*   **Minimalist Frontend:** Basic HTML, CSS, and JavaScript for form submission and displaying results.

## 2. Key Features Implemented

Throughout our session, the following major features and improvements were implemented:

### Visual Timeline View

*   **Problem Addressed:** The initial search only returned a list of free rooms, lacking a comprehensive overview of room availability throughout the day.
*   **Solution:** A visual timeline was introduced, displaying all rooms in a selected building (or all buildings) for a specific day. Each room's timeline shows booked slots (red) and free slots (green) as horizontal blocks.
*   **Benefit:** Provides an at-a-glance understanding of room schedules, making it easier to spot open slots and understand when booked rooms become free.

### Detailed Room Profile Modal

*   **Problem Addressed:** Users had no way to get more detailed information about a specific room or its full daily schedule beyond its availability at a given search time.
*   **Solution:** Clicking on any room in the timeline now triggers a sleek, non-overwhelming modal window.
*   **Benefit:** The modal provides comprehensive details:
    *   Room name and building.
    *   Capacity and amenities (e.g., Projector, Whiteboard).
    *   A clear, chronological list of the room's entire schedule for the selected day, indicating both free and booked periods (with course details).

### Enhanced Time-Based Search & Categorization

*   **Problem Addressed:** The initial time-based search was removed in favor of the timeline, but it was crucial to re-introduce direct search for users with specific time needs. The previous "highlighting" was also deemed insufficient for clarity.
*   **Solution:** The search form now allows users to optionally specify a start time and duration. When provided, the results are explicitly categorized into two distinct sections:
    *   **Available Rooms:** Rooms that are free for the *entire* specified time and duration.
    *   **Unavailable Rooms:** All other rooms, showing their full timeline for context.
*   **Benefit:** Combines the power of a direct search with the rich context of the timeline, providing immediate, unambiguous answers while still allowing users to browse other options.

### Tabbed Interface for Search Results

*   **Problem Addressed:** Displaying both "Available" and "Unavailable" rooms in a single, long scrolling list could be overwhelming.
*   **Solution:** A tabbed interface was implemented at the top of the results section, allowing users to toggle between "Available" and "Unavailable" rooms with a single click.
*   **Benefit:** Improves user experience by reducing visual clutter and providing a clear, organized way to view search results. The toggling is client-side for instant feedback.

### Comprehensive UI/UX Redesign

*   **Problem Addressed:** The initial design was basic, and subsequent changes inadvertently broke the styling, leading to a raw HTML appearance. A desire for a "sleek, modern, and unforgettable" design was expressed.
*   **Solution:** A complete overhaul of the frontend styling and structure was performed, drawing inspiration from modern, minimalist applications like Gmail and Perplexity.
*   **Benefit:**
    *   **Clean Aesthetic:** Card-based layout, refined typography, and a harmonious color palette.
    *   **Intuitive Layout:** Clear visual hierarchy, responsive design for various screen sizes.
    *   **Enhanced Visual Timeline:** Booked and free slots now feature subtle gradients and animated patterns for better visual distinction and appeal. Time markers (e.g., 7 AM, 9 AM) were added above the timeline for easy time orientation.
    *   **Micro-interactions:** Subtle animations were added to elements like buttons and modals for a more responsive and polished feel.

### Robust Sample Data Generation

*   **Problem Addressed:** The initial sample data was too small and simplistic to accurately represent a real college environment, making testing and demonstration difficult.
*   **Solution:** A Python script (`generate_sample_data.py`) was created to generate a large, realistic dataset for both `rooms.xlsx` and `timetable.xlsx`.
*   **Benefit:** Provides a comprehensive dataset for thorough testing of the application's features and performance under more realistic conditions, and serves as a clear example for users to structure their own college data.

## 3. Technical Implementation Details

This section details the specific code changes and the logic behind them.

### Backend Logic (`finder/views.py`)

The `search_rooms` view was significantly refactored to support the new features:

*   **Input Handling:** It now accepts `building`, `day`, and optionally `time` and `duration` from the `RoomSearchForm`.
*   **Comprehensive Timeline Generation:**
    *   Fetches all `Room` objects based on the selected `building` (or all if "ALL" is chosen).
    *   For each room, it queries its `ClassSchedule` entries for the selected `day`.
    *   It constructs a `timeline` list for each room, representing the entire day (7 AM to 11 PM). This timeline is composed of dictionaries, each indicating a `type` ("free" or "booked"), `start` and `end` times (as `datetime.time` objects), and `course` (if booked).
    *   Crucially, it calculates `start_percentage` and `width_percentage` for each timeline block. These percentages are used by the frontend CSS to accurately position and size the blocks on the visual timeline, ensuring a correct representation of time.
*   **Availability Check & Categorization:**
    *   If `time` and `duration` are provided in the search, the view calculates the `search_start_time` and `search_end_time`.
    *   It then iterates through each room's generated `timeline`. A room is considered "available" only if the entire `search_time` and `duration` fit within a single, uninterrupted "free" block in its timeline.
    *   Rooms are then separated into two lists: `available_rooms` and `unavailable_rooms`.
*   **Context Passing:** The view passes `form`, `available_rooms`, `unavailable_rooms`, `errors`, and a `search_performed` flag to the template.
*   **AJAX Handling:** For AJAX requests (identified by `X-Requested-With` header), it renders only the `timeline_partial.html` to update the results section dynamically.
*   **`home` function:** A simple redirect from the root URL to the `search_rooms` view was re-added to `views.py` to ensure proper routing.
*   **`upload_excel` function:** The indentation was corrected, and its core logic for processing Excel files remains.

### Room Details API (`finder/api.py`)

A new API endpoint was created to serve detailed room information for the modal:

*   **`room_details(request, room_id)` function:**
    *   Retrieves a specific `Room` object by its `id`.
    *   Fetches its `ClassSchedule` for the `day` provided in the GET parameters (defaults to Monday).
    *   Constructs a detailed `timeline` for that room, similar to the `search_rooms` view, but specifically for a single room.
    *   Returns a `JsonResponse` containing the room's attributes (name, building, capacity, amenities, photo_url) and its full daily timeline.
    *   **Bug Fix:** Ensured `start` and `end` times in the timeline blocks are consistently formatted as strings (`%H:%M`) to prevent "undefined" errors in the frontend modal.

### Frontend Interaction (`finder/static/finder/js/scripts.js`)

The JavaScript was updated to handle dynamic content loading, modal interactions, and tab switching:

*   **AJAX Search Submission:**
    *   Intercepts the search form submission.
    *   Sends an AJAX POST request to the `search_rooms` view.
    *   Receives the rendered `timeline_partial.html` and injects it into the `results-container`.
*   **Modal Trigger & Population:**
    *   An event listener on the `resultsContainer` (using event delegation) detects clicks on `.timeline-row` elements.
    *   Extracts the `data-room-id` from the clicked row.
    *   Makes an AJAX GET request to the new `/api/room/<room_id>/` endpoint.
    *   Receives the JSON response and dynamically populates the `modal-body` with room details and its full schedule.
    *   Adds the `show` class to the modal to display it.
*   **Modal Close:** Event listeners for the close button and clicking outside the modal remove the `show` class to hide it.
*   **Tab Toggling:**
    *   An event listener on the `resultsContainer` (using event delegation) detects clicks on `.tab-link` buttons.
    *   Manages `active` classes on tab links and tab content divs to show/hide the corresponding sections.

### Styling (`finder/static/finder/css/styles.css`)

The entire CSS file was rewritten to achieve the desired sleek, modern, and unforgettable design:

*   **Global Styles:** Defined a new color palette using HSL for easy theme adjustments, modern `Inter` font, consistent spacing, and subtle shadows.
*   **Layout:** Implemented a responsive flexbox/grid layout for the main content area, with a sticky sidebar for the search form.
*   **Components:**
    *   **Cards:** Defined a `.card` class for consistent styling of modules and containers.
    *   **Forms:** Clean, well-spaced form elements with clear focus states.
    *   **Buttons:** Modern, accessible button styles.
    *   **Tabs:** Visually distinct tab links with an active state indicator.
    *   **Timeline:**
        *   `timeline-header` for time markers (7 AM, 9 AM, etc.).
        *   `timeline-row` for each room's timeline.
        *   `timeline-block` for individual time segments.
        *   **Visual Enhancements:** `free` blocks use a subtle animated stripe pattern with a success color. `booked` blocks use a subtle dark stripe pattern with a danger color. This provides clear visual distinction and a dynamic feel.
    *   **Modal:** Overlay with backdrop blur, smooth fade-in animation, and clear content presentation.
*   **Responsive Design:** Media queries ensure the layout adapts gracefully to smaller screens.

### Database Model Enhancements (`finder/models.py`)

The `Room` model was extended to store more detailed information:

*   `capacity = models.PositiveIntegerField(default=0)`: Stores the maximum occupancy of the room.
*   `amenities = models.JSONField(default=list)`: Stores a list of amenities (e.g., `["Projector", "Whiteboard"]`) as a JSON array.
*   `photo_url = models.URLField(blank=True, null=True)`: Stores a URL to an image of the room.

### Forms (`finder/forms.py`)

The `RoomSearchForm` was updated to reflect the re-introduction of time-based search:

*   Re-added `time = forms.TimeField(required=False)` and `duration = forms.ChoiceField(required=False)`.
*   The `building` field now includes an "ALL" option to search across all buildings.
*   These fields are `required=False` to allow users to perform a broad timeline search without specifying a time.

### URL Configuration (`finder/urls.py` & `roomfinder/urls.py`)

*   **`finder/urls.py`:**
    *   Added `path("api/room/<int:room_id>/", api.room_details, name="room_details")` to expose the new API endpoint.
    *   Ensured `path("", views.home, name="home")` correctly redirects to the search page.
    *   Corrected the `upload_excel` path to `path("upload/", views.upload_excel, name="upload_excel")`.
*   **`roomfinder/urls.py`:** Confirmed that `path("", include("finder.urls", namespace="finder"))` correctly includes the `finder` app's URLs.

### Management Commands (`finder/management/commands/`)

*   **`load_rooms_excel.py`:** Updated to read and save the new `capacity`, `amenities`, and `photo_url` fields from `rooms.xlsx`. It now expects the file in the `sample_data` directory.
*   **`load_timetable.py`:** Updated to correctly locate `timetable.xlsx` in the `sample_data` directory.

## 4. Key Bug Fixes During Development

Several critical bugs were identified and fixed throughout the development process:

*   **`AttributeError: module 'finder.views' has no attribute 'home'` / `search_rooms`:** Caused by accidental overwrites of the `finder/views.py` file, leading to missing function definitions. Fixed by restoring the complete and correct `views.py` content.
*   **`IndentationError` in `views.py`:** A syntax error due to incorrect Python indentation. Fixed by correcting the spacing within the `upload_excel` function.
*   **`UnboundLocalError: cannot access local variable 'search_time'`:** Occurred when `search_time` and `duration` were accessed on initial page load (GET request) before being assigned a value. Fixed by initializing these variables to `None` at the beginning of the `search_rooms` function.
*   **"undefined-undefined" in Modal:** The modal was displaying "undefined" for start/end times. This was due to the `api.py` view sending `datetime.time` objects directly, and the JavaScript expecting string representations. Fixed by explicitly formatting times as strings (`"%H:%M"`) in `api.py` and ensuring `scripts.js` used the correct `start` and `end` keys.
*   **Broken CSS Linking:** Accidental overwrites of `styles.css` and incorrect linking in HTML templates led to unstyled pages. Fixed by ensuring the `styles.css` file was always complete and correctly linked in all templates.

## 5. Setup and Running the Project

To get the Campuspal Room Finder up and running:

1.  **Clone the Repository:** (Assuming you have the project files)
    ```bash
    cd D:\engineering\experiments\siara\roomfinder
    ```
2.  **Activate Virtual Environment:**
    ```bash
    my-venv\Scripts\activate
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: `requirements.txt` might need to be created or updated if not present, containing `Django`, `pandas`, `openpyxl`, etc.)*
4.  **Apply Migrations:**
    ```bash
    python manage.py makemigrations finder
    python manage.py migrate
    ```
5.  **Generate Sample Data:**
    ```bash
    python generate_sample_data.py
    ```
    This will create `rooms.xlsx` and `timetable.xlsx` in the `sample_data` directory.
6.  **Load Sample Data into Database:**
    ```bash
    python manage.py shell -c "from finder.models import Room, ClassSchedule; Room.objects.all().delete(); ClassSchedule.objects.all().delete()"
    python manage.py load_rooms_excel
    python manage.py load_timetable
    ```
    *(The first command clears existing data, the next two load the new sample data.)*
7.  **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```
8.  **Access the Application:** Open your web browser and navigate to `http://127.0.0.1:8000/`.

## 6. Future Enhancements

Based on our discussions, here are some potential future enhancements:

*   **Natural Language Search:** Integrate an LLM to allow users to search using conversational queries (e.g., "Find me a room for an hour on Tuesday afternoon in the Apollo Building with a projector").
*   **Predictive Availability:** Use machine learning to predict future room availability based on historical usage patterns.
*   **Room Booking System:** Implement functionality for users to reserve available rooms directly through the application.
*   **User Accounts & Favorites:** Allow users to create accounts, save favorite rooms, and store frequent search criteria.
*   **Admin Dashboard:** A dedicated interface for administrators to manage rooms, schedules, and user permissions.
*   **Integration with Campus Systems:** If available, integrate with official university scheduling APIs for real-time data synchronization.