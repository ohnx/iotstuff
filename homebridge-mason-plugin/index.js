// Example Air Quality Sensor Plugin
const http = require('http');

module.exports = (api) => {
  api.registerAccessory('MasonPyportalSensorPlugin', MasonPyportalSensorAccessory);
};

class MasonPyportalSensorAccessory {

  constructor(log, config, api) {
      this.log = log;
      this.config = config;
      this.api = api;

      this.Service = this.api.hap.Service;
      this.Characteristic = this.api.hap.Characteristic;

      // extract name from config
      this.name = config.name;

      // endpoint
      this.endpoint = config.endpoint;

      // information
      this.informationService = new this.Service.AccessoryInformation();
      this.informationService
        .setCharacteristic(this.Characteristic.Manufacturer, "Mason")
        .setCharacteristic(this.Characteristic.Model, "PyPortal")
        .setCharacteristic(this.Characteristic.SerialNumber, this.name)
        .setCharacteristic(this.Characteristic.FirmwareRevision, require('./package.json').version);

      // create a new Air Quality Sensor service
      this.service = new this.Service.AirQualitySensor();

      // create a new temperature sensor service
      this.serviceTemp = new this.Service.TemperatureSensor();

      // create a new Humidity Sensor service
      this.serviceHum = new this.Service.HumiditySensor();
  }

  updateData() {
        http.get(this.endpoint, (resp) => {
          let data = '';

          // A chunk of data has been received.
          resp.on('data', (chunk) => {
            data += chunk;
          });

          // The whole response has been received. Print out the result.
          resp.on('end', () => {
//            console.log(JSON.parse(data));
            data = JSON.parse(data);

            this.service
              .setCharacteristic(this.Characteristic.AirQuality, this.Characteristic.AirQuality.UNKNOWN);
            this.service
              .setCharacteristic(this.Characteristic.VOCDensity, 1000);
            this.serviceTemp
              .setCharacteristic(this.Characteristic.CurrentTemperature, data.temp);
            this.serviceHum
              .setCharacteristic(this.Characteristic.CurrentRelativeHumidity, data.humidity);
          });

        }).on("error", (err) => {
          this.log("Error: " + err.message);
        });
  }

  getServices() {
    setInterval(function() {
      this.updateData();
    }.bind(this), 1000*60);
    this.updateData();

    return [this.informationService, this.service, this.serviceTemp, this.serviceHum];
  }

  /**
   * Handle requests to get the current value of the "Air Quality" characteristic
   */
  handleAirQualityGet() {
    this.log.debug('Triggered GET AirQuality');

    // set this to a valid value for AirQuality
    const currentValue = this.Characteristic.AirQuality.UNKNOWN;

    return currentValue;
  }

  /**
   * Handle requests to get the current value of the "VOC Density" characteristic
   */
  handleVOCDensityGet() {
    this.log.debug('Triggered GET VOCDensity');

    // set this to a valid value for VOCDensity
    const currentValue = 1000;

    return currentValue;
  }

  /**
   * Handle requests to get the current value of the "Current Temperature" characteristic
   */
  handleCurrentTemperatureGet() {
    this.log.debug('Triggered GET CurrentTemperature');

    // set this to a valid value for CurrentTemperature
    const currentValue = -270;

    return currentValue;
  }


  /**
   * Handle requests to get the current value of the "Current Relative Humidity" characteristic
   */
  handleCurrentRelativeHumidityGet() {
    this.log.debug('Triggered GET CurrentRelativeHumidity');

    // set this to a valid value for CurrentRelativeHumidity
    const currentValue = 1;

    return currentValue;
  }

}

