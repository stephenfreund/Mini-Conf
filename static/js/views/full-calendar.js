/*
We use https://fullcalendar.io/
Much of this is borrowed from ACL 2020 code base.
*/

/*
See https://fullcalendar.io/docs/timeZone

The calendar treats all event dates as being in UTC without considering
the timezone offset.  So, the "events" function coerces the event dates
that come in in UTC format to be correct in the target timezone.

This means that when you want to compare the a date stored in an event
object with a "real" date, care must be taken to also convert the real
data to this non-standard rep.
*/

// Everything below uses the currentTime() function to get the current
// time.  Change time there for debugging...  See timeZones.js.

// mt is a moment object
// mirror block is 0-8 UTC.
function momentIsDuringMirrorBlock(mt) {
  const startOfMirrorBlock = moment.utc("2021-06-23T00:00Z"); // midnight...
  const offset = moment.tz
    .zone(getCurrentTimeZone())
    .utcOffset(startOfMirrorBlock);
  const hour = (mt.hour() + offset / 60) % 24;
  // console.log (mt.date())
  return hour >= 1 && hour < 8; //  && (mt.date() == 23 || mt.date() == 24 || mt.date() == 25);
}

function currentTimeRoundedToHourForScrolling() {
  return `${currentTimeMoment().format("HH")}:00:00`;
}

// /////////////

function currentTimeMomentForFiltering() {
  // See comments above about this situation.
  // We're putting now into the appropriate time zone...
  const rawNow = currentTimeMoment();
  const offset = moment.tz.zone(getCurrentTimeZone()).utcOffset(rawNow);
  const now = rawNow.subtract({ minutes: offset });
  return now;
}

function isPast(event) {
  // See comments above about this situation.
  // We're putting now into the appropriate time zone...
  const now = currentTimeMomentForFiltering().add({ minutes: -1 });
  const end = moment(event.end);
  return end.isBefore(now);
}

function isNow(event) {
  const now = currentTimeMomentForFiltering().add({ minutes: 1 });
  const start = moment(event.start);
  const end = moment(event.end);
  return start.isSameOrBefore(now) && !isPast(event);
}

function isSoon(event) {
  const now = currentTimeMomentForFiltering().add({ minutes: 1 });
  const start = moment(event.start);
  const end = moment(event.end);
  return (
    !isPast(event) &&
    !isNow(event) &&
    start.isSameOrBefore(now.add({ minutes: 15 }))
  );
}

// //////////////////

/*
config should probably include at least:
initialDate: '{{ config.calendar.start }}',
validRange: {
    start: '{{ config.calendar.start }}',
    end: '{{ config.calendar.end }}'
},
*/
async function makeBasicCalendar(
  elementId,
  config,
  calendar,
  includeLinksInEvents
) {
  const globalConfig = await API.getConfig();

  const events = JSON.parse(calendar);
  const calendarEl = document.getElementById(elementId);

  const cal = new FullCalendar.Calendar(calendarEl, {
    schedulerLicenseKey: "GPL-My-Project-Is-Open-Source",
    initialView: "timeGridWeek",
    timeZone: getCurrentTimeZone(),
    allDaySlot: false,
    // nowIndicator: true,
    now: currentTime(),
    slotLabelFormat: {
      hour: "2-digit",
      minute: "2-digit",
      meridiem: false,
      hour12: false,
    },
    eventTimeFormat: {
      hour: "2-digit",
      minute: "2-digit",
      meridiem: false,
      timeZoneName: "short",
      hour12: false,
    },
    //  eventOrder: "start,-duration,allDay,trackUID",
    themeSystem: "bootstrap",
    slotEventOverlap: false,
    height: "700px",
    events(info, successCallback, failureCallback) {
      // We need to change the time zone manually,
      // we cannot use static event data
      // Deep copy
      let tz = info.timeZone;

      if (tz === "Local") {
        tz = moment.tz.guess();
      }

      const zoned_events = JSON.parse(JSON.stringify(events));
      for (let i = 0; i < zoned_events.length; i += 1) {
        const obj = zoned_events[i];
        obj.start = moment(obj.start).tz(tz).format();
        obj.end = moment(obj.end).tz(tz).format();

        const configColor = globalConfig.calendar.colors[obj.category];
        const color = configColor || globalConfig.calendar.colors.other;
        obj.borderColor = color;
        obj.backgroundColor = color;

        obj.id = obj.UID;
        // console.log(obj.info_link)
        if (includeLinksInEvents) {
          obj.url = obj.info_link;
        }

        obj.title = obj.title.replace(
          "-- live Q&A",
          '<span class="badge badge-light ml-1 rounded-0">Q&A</a>'
        );
      }
      successCallback(zoned_events);
    },

    /* eslint-disable */
    eventOrder: [
      "start",
      "-duration",
      "allDay",
      (a, b) => {
        // console.log(`${a.category} - ${b.category}`)
        return a.category.includes("session") && b.category.includes("session")
          ? 0
          : a.category.includes("session")
          ? -1
          : b.category.includes("session")
          ? 1
          : 0;
      },
      "trackUID",
      "title",
    ],
    /* eslint-enable */

    eventClassNames(arg) {
      const start = moment.utc(arg.event.start);
      const category = arg.event.extendedProps.category
        ? arg.event.extendedProps.category
        : "unknown";
      return `
        category-${category}
        ${isPast(arg.event) ? "fc-past" : ""}
        ${isNow(arg.event) ? "fc-now" : ""}
        ${isSoon(arg.event) ? "fc-soon" : ""}
        ${momentIsDuringMirrorBlock(start) ? "fc-mirrored" : ""}
        `;
    },

    slotLaneClassNames(arg) {
      const slot = moment.utc(arg.date);
      if (momentIsDuringMirrorBlock(slot)) {
        return "fc-mirrored";
      }
      return "";
    },

    ...config,
  });

  cal.render();
  return cal;
}

/**
 * For the Grid on schedule.html.
 */

// Full Grid Calendar for complete Schedule.html page
async function makeFullGridCalendar(elementId, config, calendar) {
  const cal = makeBasicCalendar(
    elementId,
    {
      schedulerLicenseKey: "GPL-My-Project-Is-Open-Source",
      initialView: "timeGridWeek",
      scrollTime: currentTimeRoundedToHourForScrolling(),
      height: "700px",

      headerToolbar: {
        left: "today prev,next", // today",
        center: "title",
        right: "timeGridWeek,timeGridDay",
      },
      buttonText: {
        today: "Today",
        week: "Week",
        day: "Day",
      },

      eventClick(eventClickInfo) {
        const e = eventClickInfo.event;
        // Prevent reloading the current page, as we clicked
        // on a hyperlink on the current page
        eventClickInfo.jsEvent.preventDefault();

        if (e.url) {
          window.open(e.url, "_self");
          return false;
        }
        return true;
      },
      eventDidMount(info) {
        $(info.el).popover({
          title: info.event.title,
          html: true,
          content: info.timeText,
          placement: "top",
          trigger: "hover",
          container: "body",
        });
        if (
          info.view.type === "timeGridWeek" &&
          info.event.extendedProps.sideways
        ) {
          $(info.el).addClass("rotated-grid");
        }
      },
      // Render HTML from title as HTML
      eventContent(arg) {
        if (
          arg.view.type === "timeGridWeek" &&
          arg.event.extendedProps.sideways
        ) {
          return { html: arg.event.extendedProps.sideways };
        }
        return { html: arg.event.title };
      },

      // eventClassNames: function(arg) {
      //   return [ "rotated-grid" ]
      // },

      ...config,
    },
    calendar,
    true
  );

  return cal;
}

function extendedPropsAsHTMLWithDivs(event, props, categoriesWithNoButtons) {
  info = props.info_link;
  target = props.target ? props.target : "";
  // console.log(target)
  if (categoriesWithNoButtons.includes(props.category)) {
    // this case is for session titles in papers view -- we don't want the buttons.
    return `<div class="row">
          <div class="col-12 col-lg-10 pr-0">
            <div class="row">
                <div class="col-12">
                    <span class="fc-event-title-text">
                      ${info ? `<a href="${info}" target="${target}">` : ""}
                      ${props.title ? props.title : event.title}
                      ${info ? "</a>" : ""}
                      ${
                        props.subtitle && props.subtitle !== ""
                          ? `<span class='text-muted'>${props.subtitle}</span>`
                          : ""
                      }
                    </span>
                </div>
            </div>
        </div>
      </div>`;
  }
  return `<div class="row">
          <div class="col-12 col-lg-9 pr-0">
            <div class="row">
                <div class="col-12">
                    <span class="fc-event-title-text">
                      ${info ? `<a href="${info}" target="${target}">` : ""}
                      ${props.title ? props.title : event.title}
                      ${info ? "</a>" : ""}
                      ${
                        props.subtitle && props.subtitle !== ""
                          ? ` &mdash; <span class='text-muted'>${props.subtitle}</span>`
                          : ""
                      }
                    </span>
                </div>
            </div>
          </div>
          <div class="col-12 col-lg-3">
              ${eventButtons(props)}
          </div>
        </div>`;
}

function eventBody(event) {
  const props = event.extendedProps;
  return extendedPropsAsHTMLWithDivs(event, props, ["colocated-session"]);
}

// /

function makeListCalendar(elementId, config, calendar, includeLinksInEvents) {
  const cal = makeBasicCalendar(
    elementId,
    {
      headerToolbar: {
        left: "today prev,next",
        center: "title",
        right: "listWeek,listDay",
      },
      buttonText: {
        today: "Today",
        week: "Week",
        day: "Day",
      },
      initialView: "listWeek",
      height: "auto",

      eventContent(arg) {
        return { html: eventBody(arg.event) };
      },
      // Jeremy Gibbons bug: events split over midnight on multi-day list views
      //   have UTC as timezone rather than the right one.  The time is right,
      //   but the label is wrong.  This option changes it so events are listed
      //   only once, at the start time unless they go 3 hours into the next day.
      nextDayThreshold: "03:00:00",

      ...config,
    },
    calendar,
    includeLinksInEvents
  );
  return cal;
}

// //

/**
 * A list calendar with no options or buttons.  See sponsors, plenary, etc.
 */

function makeCompactListCalendar(elementId, config, calendar) {
  const merged = {
    headerToolbar: false,
    ...config,
  };
  return makeListCalendar(elementId, merged, calendar, false);
}

// //////////////

/**
 * For the full paper schedule.  See papers_schedule.html
 */

// NOTE: Do not use any height other than auto for this kind -- the rows
// don't work inside of <table> elements.
function eventPairsSideBySide(event) {
  const props = event.extendedProps;
  if (props.subEvents) {
    return `
            <div class="row">
              <div class="col-12 col-lg-6">
                  ${extendedPropsAsHTMLWithDivs(event, props.subEvents[0], [
                    "paper-session",
                  ])}
              </div>
              <div class="col-12 d-lg-none"><hr class="w-100 m-1"/>
              </div>
              <div class="col-12 col-lg-6">
                  ${extendedPropsAsHTMLWithDivs(event, props.subEvents[1], [
                    "paper-session",
                  ])}
              </div>
            </div>
            `;
  }
  return `
            <div class="col-12">
                ${extendedPropsAsHTMLWithDivs(event, props, ["paper-session"])}
            </div>`;
}

// every calender entry can have a subEvents property with *2*
// other events.  Don't include more right now...
function makeTwoColumListCalendar(elementId, config, calendar) {
  const merged = {
    eventContent(arg) {
      return { html: eventPairsSideBySide(arg.event) };
    },
    ...config,
  };
  return makeListCalendar(elementId, merged, calendar, false);
}

/**
 * Any Track that wants to hide past.  See pldi_track.html
 */

async function makeTimeSensitiveListCalendar(
  elementId,
  updateTimeId,
  config,
  calendar,
  includeLinksInEvents
) {
  const globalConfig = await API.getConfig();

  const timeOfUpdateEl = document.getElementById(updateTimeId);

  const currentDate = currentTimeMoment().format("YYYY-MM-DD");

  const cal = await makeBasicCalendar(
    elementId,
    {
      schedulerLicenseKey: "GPL-My-Project-Is-Open-Source",
      // initialView: "listMonthNoPast",
      initialView: "listMonth", // after conference -- show all
      height: "auto",

      headerToolbar: {
        left: "",
        center: "",
        right: "listMonthNoPast,listMonth",
      },

      views: {
        listMonth: {
          buttonText: "Show Past Events",
          viewClassNames: "fc-show-now",
        },
        listMonthNoPast: {
          type: "listMonth",
          buttonText: "Hide Past Events",
          viewClassNames: "fc-show-now fc-hide-past",
          validRange: {
            start: currentDate,
          },
        },
      },

      eventContent(arg) {
        return { html: eventBody(arg.event) };
      },
      // Same as in list views for the time sensitive calendar on the home page...
      nextDayThreshold: "03:00:00",

      ...config,
    },
    calendar,
    includeLinksInEvents
  );

  cal.updateToCurrentTime = function () {
    cal.refetchEvents();

    const mt = currentTimeMoment();
    const gmtSuffix = gmtSuffixForMoment(mt);
    timeOfUpdateEl.innerHTML = `${mt.format("HH:mm")} ${gmtSuffix}`;
  };

  const mt = currentTimeMoment();
  const gmtSuffix = gmtSuffixForMoment(mt);
  timeOfUpdateEl.innerHTML = `${mt.format("HH:mm")} ${gmtSuffix}`;

  cal.render();

  // Do I need to be polite in some way with interval tasks?
  const interval = setInterval(function () {
    $('[data-toggle="tooltip"]').tooltip("dispose");
    cal.updateToCurrentTime();
    $('[data-toggle="tooltip"]').tooltip({ delay: { show: 1000, hide: 100 } });
  }, globalConfig.calendar_refresh_interval);

  window.onunload = () => {
    clearInterval(interval);
  };

  return cal;
}

/**
 * PLDI Tracks calendar
 */

async function makePLDIListCalendar(elementId, updateTimeId, config, calendar) {
  const calendarEl = document.getElementById(elementId);

  const cal = await makeTimeSensitiveListCalendar(
    elementId,
    updateTimeId,
    {
      headerToolbar: {
        left: "summary,details",
        center: "",
        right: "listMonthNoPast,listMonth",
      },

      customButtons: {
        summary: {
          text: "Summary",
          click(mouseEvent, htmlElement) {
            $(".fc-summary-button").addClass("active");
            $(".fc-details-button").removeClass("active");
            calendarEl.classList.add("fc-hide-details");
            calendarEl.classList.remove("fc-hide-summary");
          },
        },
        details: {
          text: "Details",
          click(mouseEvent, htmlElement) {
            $(".fc-summary-button").removeClass("active");
            $(".fc-details-button").addClass("active");
            calendarEl.classList.remove("fc-hide-details");
            calendarEl.classList.add("fc-hide-summary");
          },
        },
      },

      ...config,
    },
    calendar,
    false
  );

  $(".fc-summary-button").addClass("active");

  return cal;
}

/** *
 * Front Page.  See index.html
 */

function extendedPropsAsHTMLFrontPage(event) {
  props = event.extendedProps;
  info = props.info_link;
  return `
            <span class="fc-event-title-text">
              ${
                props.conf_abbrev
                  ? `<span class="px-1 mr-2 py-0 full-calendar-prefix">${props.conf_abbrev}</span>`
                  : ""
              }
              ${info ? `<a href="${info}" target="">` : ""}
              ${props.title ? props.title : event.title}
              ${info ? "</a>" : ""}
              ${
                props.subtitle && props.subtitle !== ""
                  ? ` &mdash; <span class='text-muted'>${props.subtitle}</span>`
                  : ""
              }
            </span>
            <div class="float-right" style="width:30%">
                ${/* eventButtons(props) */ ""}
            </div>
            `;
}

async function makeFrontPageCalendar(
  elementId,
  timeOfUpdateId,
  config,
  calendar
) {
  return makeTimeSensitiveListCalendar(
    elementId,
    timeOfUpdateId,
    {
      headerToolbar: false,
      // initialView: "listMonthNoPast",
      initialView: "listMonth", // after conference -- show all
      eventTimeFormat: {
        hour: "2-digit",
        minute: "2-digit",
        timeZoneName: "short",
        meridiem: false,
        hour12: false,
      },

      eventContent(arg) {
        return { html: extendedPropsAsHTMLFrontPage(arg.event) };
      },

      ...config,
    },
    calendar,
    false
  );
}

function contentForFullSchedule(event) {
  props = event.extendedProps;
  info = props.info_link;
  return `<div class="row">
            <div class="col-12">
                <span class="fc-event-title-text">
                  ${
                    props.conf_abbrev
                      ? `<span class="px-1 mr-2 py-1 full-calendar-prefix">${props.conf_abbrev}</span>`
                      : ""
                  }
                  ${info ? `<a href="${info}" target="">` : ""}
                  ${props.title ? props.title : event.title}
                  ${
                    props.subtitle && props.subtitle !== ""
                      ? ` &mdash; <span class='text-muted'>${props.subtitle}</span>`
                      : ""
                  }
                  ${info ? "</a>" : ""}
                </span>
            </div>
         </div>`;
}

// function contentForFullSchedule(event) {
//   props = event.extendedProps;
//   info = props.info_link;
//   return `<div class="row">

//           <div class="col-12 col-lg-9 pr-0">
//             <div class="row">
//                 <div class="col-12">
//                     <span class="fc-event-title-text">
//                       ${
//                         props.conf_abbrev
//                           ? `<span class="px-1 mr-2 py-1 full-calendar-prefix">${props.conf_abbrev}</span>`
//                           : ""
//                       }
//                       ${info ? `<a href="${info}" target="">` : ""}
//                       ${props.title ? props.title : event.title}
//                       ${
//                         props.subtitle && props.subtitle !== ""
//                           ? ` &mdash; <span class='text-muted'>${props.subtitle}</span>`
//                           : ""
//                       }
//                       ${info ? "</a>" : ""}
//                     </span>
//                 </div>
//             </div>
//         </div>
//         <div class="col-12 col-lg-3">
//             ${/* eventButtons(props) */ ""}
//         </div>
//       </div>`;
// }

async function makeFullDetailedSchedule(
  elementId,
  timeOfUpdateId,
  config,
  calendar
) {
  return makeTimeSensitiveListCalendar(
    elementId,
    timeOfUpdateId,
    {
      // initialView: "listDayNoPast",
      initialView: "listDay", // after conference -- show all
      titleFormat: {
        // will produce something like "Tuesday, September 18, 2018"
        month: "long",
        year: "numeric",
        day: "numeric",
        weekday: "long",
      },
      listDayFormat: false,

      headerToolbar: {
        left: "today prev,next", // today",
        center: "title",
        right: "listDayNoPast,listDay",
      },

      views: {
        listDay: {
          buttonText: "Show Past Events",
          viewClassNames: "fc-show-now",
        },
        listDayNoPast: {
          type: "listDay",
          buttonText: "Hide Past Events",
          viewClassNames: "fc-show-now fc-hide-past",
          validRange: {
            start: currentTimeMomentForFiltering().format("YYYY-MM-DD"),
          },
        },
      },

      eventContent(arg) {
        return { html: contentForFullSchedule(arg.event) };
      },

      // for full days, it works fine to have events stretch across midnight.
      // No need to be special in this calendar.
      nextDayThreshold: "00:00:00",

      ...config,
    },
    calendar,
    false
  );
}

// hide sessions!  perhaps even workshop-sessions?
