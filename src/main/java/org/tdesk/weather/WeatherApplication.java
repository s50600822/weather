package org.tdesk.weather;

import java.io.IOException;
import java.net.Inet6Address;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.Collections;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import org.apache.commons.validator.routines.InetAddressValidator;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;


import static java.util.stream.Collectors.toSet;

@SpringBootApplication
public class WeatherApplication {

	public static void main(String[] args) {
		SpringApplication.run(WeatherApplication.class, args);

		String fileName = "Z:\\dev\\code\\weather\\src\\main\\resources\\histogram_input";

		//read file into stream, try-with-resources
		Set<String> ipmaybe = Collections.emptySet();
		try (Stream<String> stream = Files.lines(Paths.get(fileName))) {
			ipmaybe = stream.parallel()
					.flatMap(l -> Arrays.stream(l.split("\t")))
					.filter(WeatherApplication::couldBeIp)
					.collect(toSet());
			System.out.println(ipmaybe.size());
//			Set<String> ips = stream.parallel()
//					.map(WeatherApplication::process)
//					.flatMap(Set::parallelStream)
//					.collect(Collectors.toSet());
//			ips.forEach(System.out::println);
//			System.out.println(ips.size());
		} catch (IOException e) {
			e.printStackTrace();
		}
		Set<String> ips = ipmaybe.parallelStream().filter(WeatherApplication::isValidInetAddress)
				.collect(toSet());
		System.out.println(ips.size());
		ips.forEach(System.out::println);
	}

	public static Set<String> process(String line){
		return Arrays.stream(line.split("\t"))
				// filter not empty first
				.parallel()
				.filter(WeatherApplication::isValidInetAddress)
				.collect(toSet());
	}

	public static boolean couldBeIp(String s){
		if(null == s || s.isBlank() || s.length() < 7 || s.length() >39){
			return false;
		}
		return true;
	}

	public static boolean isValidInetAddress(final String address) {
		if (InetAddressValidator.getInstance().isValid(address)) {
			return true;
		}
		//not an IPV4 address, could be IPV6?
		try {
			return InetAddress.getByName(address) instanceof Inet6Address;
		} catch (final UnknownHostException ex) {
			return false;
		}
	}
}
