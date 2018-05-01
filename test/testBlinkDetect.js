// // test the openData
// const openData = require('./../src/blink/blink');
//
// describe('blink', function () {
//   before(function () {
//       data = openData.loadJSON("test/data/data-2018-5-1-11-23-10-TESTDATA-5-BLINKS.json");
//   });
//   describe('detectBlinks', function () {
//     it('5 blinks should be detected', function () {
//
//       data.forEach(function(sample) {
//           blink.getBlinks(sample);
//       });
//
//       assert.equal(blink.getBlinkcount(), 5);
//     });
//
//   });
//   after(function () {
//     data = null;
//   });
// });