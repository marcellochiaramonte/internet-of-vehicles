package de.rub.enesys.ovms3lite.mapper;

import de.rub.enesys.ovms3lite.dto.output.LocationForList;
import de.rub.enesys.ovms3lite.model.Location;
import org.mapstruct.Mapper;
import org.mapstruct.NullValuePropertyMappingStrategy;
import org.mapstruct.ReportingPolicy;
import org.mapstruct.factory.Mappers;

import java.util.List;

@Mapper(unmappedSourcePolicy = ReportingPolicy.IGNORE,
        nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.SET_TO_DEFAULT)
public interface LocationMapper {
    LocationMapper INSTANCE = Mappers.getMapper(LocationMapper.class);

    List<LocationForList> locationToLocationList(List<Location> locationList);

    LocationForList locationToLocation(Location loc);

}
