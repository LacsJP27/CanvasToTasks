import datetime
import os.path
import pickle

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar", "https://www.googleapis.com/auth/tasks"]


def main():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    serviceC = build("calendar", "v3", credentials=creds)
    serviceT = build("tasks", "v1", credentials=creds)

   
    def create_tasks(serviceT, tasklist_id='@default', title='New Task', notes=None, due=None):
        task = {
          'title' : title,
          'notes' : notes,
          'due' : due
        }
        result = serviceT.tasks().insert(tasklist='@default', body=task).execute()
        print(f'Task created: {result.get("title")}')

 # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming 10 events")
    events_result = (
        serviceC.events()
        .list(
            calendarId="22vdlb77g7b9i28ah3g2hj0nb7s0iv8u@import.calendar.google.com",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return

    #building tasks list with canvas events
    #Call the Tasks API
    
    # Prints the start and name of the next 10 events
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"])
    #   start_datetime = datetime.datetime.strptime(start, "%Y-%m-%rT%H:%M:%SZ")
    #   start_formatted = start_datetime.isoformat() + "Z"
      print(start + "T00:00:00Z")
      start_formatted = start + "T00:00:00Z"
      create_tasks(serviceT, tasklist_id='@default',title = event.get('summary','No Title'), notes="auto-generated from Canvas", due=start_formatted)
      print(start)
  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  
  main()