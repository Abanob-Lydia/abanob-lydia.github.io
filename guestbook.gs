/**
 * Wedding guestbook backend — free, stored in your own Google Sheet.
 * 1. Create a new Google Sheet. Menu: Extensions → Apps Script.
 * 2. Delete everything there, paste this whole file, click Save.
 * 3. Deploy → New deployment → type "Web app".
 *    Execute as: Me · Who has access: Anyone → Deploy → allow access.
 * 4. Copy the Web app URL (ends with /exec) and paste it into index.html:
 *    const GUESTBOOK = 'https://script.google.com/macros/s/....../exec';
 * To hide a wish, just delete its row in the sheet.
 */
function sheet_() {
  const sh = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  if (sh.getLastRow() === 0) sh.appendRow(['time', 'name', 'message']);
  return sh;
}
function doGet() {
  const rows = sheet_().getDataRange().getValues().slice(1)
    .filter(r => r[1] && r[2])
    .map(r => ({ time: r[0], name: String(r[1]), message: String(r[2]) }))
    .reverse().slice(0, 300);
  return ContentService.createTextOutput(JSON.stringify(rows)).setMimeType(ContentService.MimeType.JSON);
}
function doPost(e) {
  const d = JSON.parse(e.postData.contents || '{}');
  const name = String(d.name || '').trim().slice(0, 60);
  const message = String(d.message || '').trim().slice(0, 600);
  if (name && message) sheet_().appendRow([new Date(), name, message]);
  return ContentService.createTextOutput(JSON.stringify({ ok: true })).setMimeType(ContentService.MimeType.JSON);
}
