package de.rub.enesys.ovms3lite.service;

import de.rub.enesys.ovms3lite.dto.input.VehicleEventInput;
import de.rub.enesys.ovms3lite.dto.output.VehicleEventForList;
import de.rub.enesys.ovms3lite.mapper.VehicleEventMapper;
import de.rub.enesys.ovms3lite.model.VehicleEvent;
import de.rub.enesys.ovms3lite.repository.VehicleEventRepository;
import de.rub.enesys.ovms3lite.repository.MetricRepository;
import de.rub.enesys.ovms3lite.repository.VehicleRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.concurrent.atomic.AtomicReference;
import java.util.stream.Collectors;

@Service
public class VehicleEventService {

    @Autowired
    private VehicleEventRepository vehicleEventRepository;

    @Autowired
    private MetricRepository metricRepository;

    @Autowired
    private VehicleRepository vehicleRepository;

    @Autowired
    private VehicleEventMapper vehicleEventMapper;

    public VehicleEvent createVehicleEvent(Long timestamp, String value, String carId, Integer metricId){
        AtomicReference<VehicleEvent> createdEvent = new AtomicReference<>(null);
        metricRepository.findOneById(metricId).ifPresent(metric->{
            vehicleRepository.findOneById(carId).ifPresent(vehicle -> {
                VehicleEvent vehicleEvent = new VehicleEvent();
                vehicleEvent.setMetric(metric);
                vehicleEvent.setTimestamp(timestamp);
                vehicleEvent.setValue(value);
                vehicleEvent.setVehicle(vehicle);
                createdEvent.set(vehicleEventRepository.save(vehicleEvent));
            });
        });
        return createdEvent.get();
    }

    public void createMultipleVehicleEvents(String carId, List<VehicleEventInput> eventList){
            vehicleRepository.findOneById(carId).ifPresent(vehicle -> {
                eventList.forEach(ev->{
                    VehicleEvent vehicleEvent = new VehicleEvent();
                    metricRepository.findOneById(ev.getId()).ifPresent(m->{
                        vehicleEvent.setMetric(m);
                    });
                    vehicleEvent.setTimestamp(ev.getT());
                    vehicleEvent.setValue(ev.getV());
                    vehicleEvent.setVehicle(vehicle);
                   vehicleEventRepository.save(vehicleEvent);
                });
            });
    }

    public List<VehicleEventForList> getEventsFilterByTimeAndMetric(String vehicleUuid, Integer metricId, Long startTimestamp, Long endTimestamp){
        AtomicReference<List<VehicleEvent>> eventList = new AtomicReference<>();
        vehicleRepository.findOneById(vehicleUuid).ifPresent(vehicle -> {
            System.out.println("found car");
            eventList.set(vehicle.getVehicleEventList()
                    .stream()
                    .filter(event -> (event.getTimestamp() >= startTimestamp && event.getTimestamp() <= endTimestamp))
                    .filter(event -> event.getMetric().getId().equals(metricId))
                    .sorted(Comparator.comparing(VehicleEvent::getTimestamp))
                    .collect(Collectors.toList()));
        });
        return vehicleEventMapper.eventListToEventWithoutUuid(eventList.get());
    }

    public List<VehicleEventForList> getAll(){
        return vehicleEventMapper.eventListToEventWithoutUuid((List<VehicleEvent>) vehicleEventRepository.findAll());
    }




}
