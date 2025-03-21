package de.rub.enesys.ovms3lite.controller;

import de.rub.enesys.ovms3lite.model.Metric;
import de.rub.enesys.ovms3lite.repository.MetricRepository;
import de.rub.enesys.ovms3lite.service.VehicleEventService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class MetricController extends BaseRestController{
    @Autowired
    private MetricRepository metricRepository;

    @Autowired
    private VehicleEventService vehicleEventService;

    @GetMapping("metrics/all")
    List<Metric> findAllMetrics(){
        return (List<Metric>) metricRepository.findAll();
    }


}
