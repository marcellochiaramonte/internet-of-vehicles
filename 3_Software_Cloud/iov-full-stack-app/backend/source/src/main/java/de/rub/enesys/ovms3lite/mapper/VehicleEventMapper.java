package de.rub.enesys.ovms3lite.mapper;

import de.rub.enesys.ovms3lite.dto.input.VehicleEventInput;
import de.rub.enesys.ovms3lite.dto.output.VehicleEventForList;
import de.rub.enesys.ovms3lite.model.VehicleEvent;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.NullValuePropertyMappingStrategy;
import org.mapstruct.ReportingPolicy;
import org.mapstruct.factory.Mappers;

import java.util.List;

@Mapper(unmappedSourcePolicy = ReportingPolicy.IGNORE,
        nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.SET_TO_DEFAULT)
public interface VehicleEventMapper {
    VehicleEventMapper INSTANCE = Mappers.getMapper(VehicleEventMapper.class);

    List<VehicleEventForList> eventListToEventWithoutUuid(List<VehicleEvent> vehicleEventList);


    @Mapping(target = "timestamp", source = "t")
    @Mapping(target = "value", source = "v")
    VehicleEvent vehicleEventOutput(VehicleEventInput input);
}
