/* eslint no-var: "off", vars-on-top: "off" */

// ////

// A Cookie to stash the current time zone.
// Use this *everywhere* you need to convert dates.

function setCurrentTimeZone(tz) {
  if (tz === "Local") {
    tz = moment.tz.guess();
  }
  window.localStorage.setItem("miniconf-timezone", tz);
}

var cachedTimeZone;

function getCurrentTimeZone() {
  if (cachedTimeZone) {
    return cachedTimeZone;
  }
  const tz = getUrlParameter("tz");
  if (tz != null && tz !== "") {
    setCurrentTimeZone(tz);
    cachedTimeZone = tz;
    return cachedTimeZone;
  }
  const cookie = window.localStorage.getItem("miniconf-timezone");

  if (cookie != null && cookie !== "") {
    cachedTimeZone = cookie;
    return cachedTimeZone;
  }
  const guess = moment.tz.guess();
  setCurrentTimeZone(guess);
  cachedTimeZone = guess;
  return cachedTimeZone;
}

var fakeTime; // Fake Time For Debugging -- set to use it everywhere

function currentTime() {
  if (fakeTime) {
    return fakeTime.format();
  }
  return moment().format();
}

// Convenience function to get the current time as a moment in the current
// time zone.
function currentTimeMoment() {
  return moment.utc(currentTime()).tz(getCurrentTimeZone());
}

// Convenience function to get the current time as a moment in GMT.
function currentTimeMomentGMT() {
  return moment.utc(currentTime()).tz("GMT");
}

function gmtSuffixForMoment(atime) {
  var t = atime.format("Z");
  if (t.endsWith(":00")) {
    t = t.slice(0, -3);
  }
  if (t.startsWith("0")) {
    t = t.slice(1);
  } else if (t.startsWith("-0")) {
    t = `-${t.slice(2)}`;
  }
  return `GMT${t}`;
}

function gmtSuffixForCurrentMoment() {
  return gmtSuffixForMoment(currentTimeMoment());
}

// / For Debugging -- matches code in base.html.

function updateFakeTime() {
  const element = document.getElementById("fakeTimeId");
  if (element) {
    element.innerHTML = `${currentTimeMoment().format(
      "llll"
    )} <br> UTC: ${currentTime()} `;
  }
}

// Call this to initialize the fake time to t.
function setFakeTime(t) {
  fakeTime = moment.utc(t);
  updateFakeTime();
}

// Step fake time by number of minutes
function stepTime(min) {
  fakeTime = fakeTime.add({ minutes: min });
  updateFakeTime();
}

function fastForward() {
  setInterval(() => {
    stepTime(1);
  }, 1000);
}

// /// From Neurips /////

function getTimezone() {
  return getCurrentTimeZone();
}

function formatDate(element) {
  const current_tz = getTimezone();
  const text = element.text().trim();
  const atime = moment(text).clone().tz(current_tz);
  const gmtSuffix = `&nbsp; ${gmtSuffixForMoment(atime)}`;
  const str = atime.format("ddd HH:mm");
  element.html(`${str} ${gmtSuffix}`);
}

function formatDateTime(element) {
  const current_tz = getTimezone();
  const text = element.text().trim();
  const atime = moment(text).clone().tz(current_tz);
  const gmtSuffix = `&nbsp; ${gmtSuffixForMoment(atime)}`;
  const str = atime.format("ddd HH:mm");
  element.html(`${str} ${gmtSuffix}`);
}

function formatTimeSpan(element, includeGMT) {
  const current_tz = getTimezone();
  const parts = element.text().trim().split(" - ");
  // console.log(parts, "--- parts", element.text());
  const start = parts[0].trim();
  const end = parts[1].trim();

  const starttime = moment(start).clone().tz(current_tz);
  const endtime = moment(end).clone().tz(current_tz);

  if (includeGMT) {
    gmtSuffix = `&nbsp; ${gmtSuffixForMoment(starttime)}`;
  } else {
    gmtSuffix = "";
  }

  // if(starttime.diff(endtime, "days") <= 0) // Making difference between the "D" numbers because the diff function
  // seems like not considering the timezone
  if (starttime.format("D") === endtime.format("D")) {
    element.html(
      `${starttime.format("ddd HH:mm")} &ndash; ${endtime.format(
        "HH:mm"
      )} ${gmtSuffix}`
    );
    // element.html(
    //   `${starttime.format("HH:mm")} &ndash; ${endtime.format(
    //     "HH:mm ~"
    //   )} ${gmtSuffix}`
    // );
  } else {
    element.html(
      `${starttime.format("ddd HH:mm")} &ndash; ${endtime.format(
        "ddd HH:mm"
      )} ${gmtSuffix}`
    );
  }
}

function formatTimeSpanWithDays(element, includeGMT) {
  const current_tz = getTimezone();
  const parts = element.text().trim().split(" - ");
  const start = parts[0].trim();
  const end = parts[1].trim();

  const starttime = moment(start).clone().tz(current_tz);
  const endtime = moment(end).clone().tz(current_tz);

  if (includeGMT) {
    gmtSuffix = `&nbsp; ${gmtSuffixForMoment(starttime)}`;
  } else {
    gmtSuffix = "";
  }

  element.html(
    `${starttime.format("ddd HH:mm")} &ndash; ${endtime.format(
      "ddd HH:mm"
    )} ${gmtSuffix}`
  );
}

function formatTime(element) {
  const current_tz = getTimezone();
  const atime = moment(element.text()).clone().tz(current_tz);
  const gmtSuffix = `&nbsp; ${gmtSuffixForMoment(atime)}`;
  element.html(`${atime.format("HH:mm")} ${gmtSuffix}`);
}

function timeZoneStart() {
  const current_tz = getTimezone();
  $("#tzCurrent").html(moment().tz(current_tz).format("Z"));

  // find all parseable dates and localize them
  $(".format-just-date").each((_i, element) => {
    formatDate($(element));
  });

  $(".format-date").each((_i, element) => {
    formatDateTime($(element));
  });

  $(".format-date-span").each((_i, element) => {
    formatTimeSpan($(element, true));
  });

  $(".format-date-span-short").each((_i, element) => {
    formatTimeSpan($(element), false);
  });

  $(".format-date-span-with-days").each((_i, element) => {
    formatTimeSpanWithDays($(element), true);
  });

  $(".format-date-span-full").each((_i, element) => {
    formatTimeSpan($(element), true);
  });

  $(".format-time").each((_i, element) => {
    formatTime($(element));
  });
}

$(document).ready(() => {
  timeZoneStart();
});
