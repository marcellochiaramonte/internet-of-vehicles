package de.rub.enesys.ovms3lite.configuration.websocket;

import org.springframework.messaging.simp.config.MessageBrokerRegistry;
import org.springframework.web.socket.config.annotation.*;

public class WebSocketConfiguration implements  WebSocketMessageBrokerConfigurer   {

    @Override
    public void configureMessageBroker(MessageBrokerRegistry registry) {
        registry.enableSimpleBroker("/topic");
        registry.setApplicationDestinationPrefixes("/app");
    }

    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        registry.addEndpoint("/websocket")
                .setAllowedOrigins("*");
        registry.addEndpoint("/sockjs")
                .withSockJS();
    }
}
