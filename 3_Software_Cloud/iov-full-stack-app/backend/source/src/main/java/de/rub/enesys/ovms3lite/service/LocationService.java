package de.rub.enesys.ovms3lite.service;

import de.rub.enesys.ovms3lite.dto.input.LocationInput;
import de.rub.enesys.ovms3lite.dto.output.LocationForList;
import de.rub.enesys.ovms3lite.mapper.LocationMapper;
import de.rub.enesys.ovms3lite.model.Location;
import de.rub.enesys.ovms3lite.repository.LocationRepository;
import de.rub.enesys.ovms3lite.repository.VehicleRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Comparator;
import java.util.List;
import java.util.concurrent.atomic.AtomicReference;
import java.util.stream.Collectors;


@Service
public class LocationService {

    @Autowired
    private VehicleRepository vehicleRepository;

    @Autowired
    private LocationRepository locationRepository;

    @Autowired
    private LocationMapper locationMapper;

    public Location createNewLocation(Long timestamp,Double latitude,Double longitude,String carId){
        AtomicReference<Location> createdLocation = new AtomicReference<>(null);
        vehicleRepository.findOneById(carId).ifPresent(vehicle -> {
            createdLocation.set(locationRepository.save(new Location(timestamp,latitude,longitude,vehicle)));
        });
        return createdLocation.get();
    }

    public List<LocationForList> filterLocations( String carId,Long startTimestamp,Long endTimestamp){
        AtomicReference<List<Location>> locationList = new AtomicReference<>();
        vehicleRepository.findOneById(carId).ifPresent(vehicle -> {
            locationList.set(
                    vehicle.getLocationList().stream()
                    .filter(location -> (location.getTimestamp() >= startTimestamp && location.getTimestamp() <= endTimestamp))
                    .collect(Collectors.toList()));

        });
        return locationMapper.locationToLocationList(locationList.get());
    }

    public LocationForList getLastLocation(String carId){
        AtomicReference<Location> location = new AtomicReference<>();
        vehicleRepository.findOneById(carId).ifPresent(vehicle -> {
            System.out.println("found car "+vehicle.getId());
            long count = vehicle.getLocationList().size();
            if(count>0){
                vehicle.getLocationList().stream()
                        .sorted(Comparator.comparing(Location::getTimestamp))
                        .skip(count-1).findAny().ifPresent(location::set);
            }

        });
        return locationMapper.locationToLocation(location.get());
    }

    public void createMultipleLocation(String carId, List<LocationInput> locationList){
        vehicleRepository.findOneById(carId).ifPresent(vehicle -> {
            locationList.forEach(loc->{
                Location location = new Location();
                location.setVehicle(vehicle);
                location.setTimestamp(loc.getT());
                location.setLatitude(loc.getLat());
                location.setLongitude(loc.getLon());
                locationRepository.save(location);
            });
        });
    }

}
