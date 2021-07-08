// helpers to generate pill buttons for PLDI events.

function possibleButton(title, link, color, tip, extras = "") {
  return `<a href="${link}" ${extras} class="badge pldi-pill badge-${color}" data-toggle="tooltip" data-placement="top" title="${tip}">
    ${title}</a>`;
}

function streamButton(event) {
  if (event.track) {
    return possibleButton(
      event.track.location,
      event.track.link,
      "info text-white",
      `Go to Track ${event.track.location}`
    );
  }
  return "";
}

function gatherButton(event) {
  if (event.gather) {
    title = event.gather.location;
    if (title.length > 6) {
      title = title.substring(7);
    }

    return possibleButton(
      `<i class="fas fa-users"></i>&nbsp;&nbsp;${title}`,
      event.gather.link,
      "success text-white",
      `Go to Gather ${title}`,
      "target='_blank'"
    );
  }
  return "";
}

function zoomButton(event) {
  if (event.zoom) {
    title = `<i class="fas fa-video"></i>&nbsp;&nbsp;${event.zoom.location}`;

    return possibleButton(
      title,
      event.zoom.link,
      "primary text-white",
      "Join this event in Zoom",
      "target='_blank'"
    );
  }
  return "";
}

function talkButton(event) {
  if (event.talk) {
    title = `${event.talk.location}`;

    return possibleButton(
      title,
      event.talk.link,
      "secondary text-white",
      "Watch the video",
      "target='_blank'"
    );
  }
  return "";
}

function eventButtons(event) {
  return (
    talkButton(event) +
    streamButton(event) +
    zoomButton(event) +
    gatherButton(event)
  );
}

setTimeout(function () {
  $('[data-toggle="tooltip"]').tooltip({ delay: { show: 500, hide: 0 } });
}, 1000);

function dayAbbrev(day) {
  return day;
}
